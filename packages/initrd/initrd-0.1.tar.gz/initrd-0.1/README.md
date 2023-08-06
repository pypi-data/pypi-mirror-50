The Linux kernel can be made to create an initial RAM disk using the gen_init_cpio.c
program found under /usr/src/linux/usr/.  The program makes use of a spec file to 
determine the device nodes, links and directories to be included, which means there is
no requirement to run as root.  This is great for generating initrds but lacks the
capability to unpack them.

This module includes code to unpack an initrd (assuming gzip or lzma compression)
and also wraps the gen_init_cpio.c program to re-pack it.  It's useful for automated
modification of installer ISOs where you need to patch the setup scripts
before they run.
