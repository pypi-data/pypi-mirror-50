

import os
import six
import shutil
try:
    import lzma
except ImportError:
    from backports import lzma
import gzip
from subprocess import Popen, PIPE
from distutils.unixccompiler import UnixCCompiler


TYPE_SOCKET = 0o0140000
TYPE_SLINK = 0o0120000
TYPE_FILE = 0o0100000
TYPE_NODE_BLOCK = 0o0060000
TYPE_DIR = 0o0040000
TYPE_NODE_CHAR = 0o0020000
TYPE_PIPE = 0o0010000


def read8(fp):
    return int(fp.read(8), 16)


def padding(fp):
    while fp.tell() & 3:
        fp.read(1)


def extract_one(fp, out_dir, fp_out, inodes):
    if fp.read(6) != b"070701":
        raise ValueError("Only 'new' CPIO format is accepted")
    ino = read8(fp)
    cpio_mode = read8(fp)
    uid = read8(fp)
    gid = read8(fp)
    _nlink = read8(fp)
    mtime = read8(fp)
    filesize = read8(fp)
    _devmajor = read8(fp)
    _devminor = read8(fp)
    rdevmajor = read8(fp)
    rdevminor = read8(fp)
    namesize = read8(fp) - 1
    _check = read8(fp)

    # read name
    name = fp.read(namesize)
    # terminator
    fp.read(1)

    if name == b"TRAILER!!!":
        return False
    padding(fp)

    if name == b".":
        return True

    # Now the file, if there is one.
    file_data = fp.read(filesize)
    padding(fp)

    entry = 0o0170000 & cpio_mode
    mode = cpio_mode & 0o7777

    if entry == TYPE_SOCKET:
        fp_out.write(b"sock %s %o %d %d\n" % (name, mode, uid, gid))
    elif entry == TYPE_SLINK:
        fp_out.write(b"slink %s %s %o %d %d\n" % (name, file_data, mode, uid, gid))
    elif entry == TYPE_FILE:
        if ino in inodes:
            raise ValueError("Hard links unsupported: %r -> %r" % (name, inodes[ino]))
        inodes[ino] = name
        path = os.path.join(out_dir, name.decode("utf-8"))
        dir_name = os.path.dirname(path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        fp_out.write(b"file %s %s %o %d %d\n" % (name, path.encode("utf-8"), mode, uid, gid))
        open(path, "wb").write(file_data)
        os.utime(path, (mtime, mtime))
    elif entry == TYPE_NODE_BLOCK:
        fp_out.write(b"nod %s %o %d %d b %d %d\n" % (name, mode, uid, gid, rdevmajor, rdevminor))
    elif entry == TYPE_DIR:
        fp_out.write(b"dir %s %o %d %d\n" % (name, mode, uid, gid))
    elif entry == TYPE_NODE_CHAR:
        fp_out.write(b"nod %s %o %d %d c %d %d\n" % (name, mode, uid, gid, rdevmajor, rdevminor))
    elif entry == TYPE_PIPE:
        fp_out.write(b"dir %s %o %d %d\n" % (name, mode, uid, gid))
    else:
        raise ValueError("Invalid type")

    return True


def get_file_opener(path):
    """
    :param path: Path to the initrd
    :return: Open function to open the file with the right decompression
    """
    p = Popen(["file", path], stdout=PIPE)
    out, err = p.communicate("")
    if out.find(b"gzip") != -1:
        return gzip.open, "gzip"
    elif out.find(b"XZ compressed data") != -1:
        return lzma.open, "lzma"
    raise ValueError("Unexpected compression type %r" % out)


def extract(cpio_path, out_dir):
    """
    :param cpio_path: cpio archive file (gz or lzma compressed)
    :param out_dir: directory into which to output files
    :return: (spec_content, type_of_compression)
    """
    # Detect the file type
    opener, type_str = get_file_opener(cpio_path)
    fp = opener(cpio_path)
    spec_fp = six.BytesIO()
    inodes = {}
    while extract_one(fp, out_dir, spec_fp, inodes):
        pass

    return spec_fp.getvalue(), type_str


def get_file_write_handle(name, output):
    """
    :param name: type of compression
    :param output: output initrd file to open
    :return:
    """
    if name == "gzip":
        return gzip.open(output, "wb")
    if name == "lzma":
        return lzma.open(output, "wb", check=lzma.CHECK_CRC32)
    raise ValueError("Unexpected compression type")


def compile_exe():
    user = os.path.expanduser("~/.pyinitrd")
    if not os.path.exists(user):
        os.mkdir(user)

    src = os.path.join(user, "gen_init_cpio.c")
    if not os.path.exists(src):
        orig = "/usr/src/linux/usr/gen_init_cpio.c"
        if not os.path.exists(orig):
            Exception("Requires Linux kernel sources in %r" % orig)
        shutil.copyfile(orig, src)

    compiler = UnixCCompiler()

    obj = os.path.join(user, "gen_init_cpio.o")
    if not os.path.exists(obj):
        compiler.compile(["gen_init_cpio.c"], user)

    exe = os.path.join(user, "gen_init_cpio")
    if not os.path.exists(exe):
        print("compiling")
        compiler.link_executable([obj], exe, user)

    return exe


def gen_init_cpio(spec, output_initrd, compression_type_str):
    """
    :param spec: spec file in format expected by gen_init_cpio
    :param output_initrd: initrd to write out
    :param compression_type_str: type of compression to use.
    :return:
    """
    compile_exe()
    p = Popen([compile_exe(), spec], stdout=PIPE)
    data = p.communicate("")[0]
    fp = get_file_write_handle(compression_type_str, output_initrd)
    fp.write(data)
    fp.close()

