#!/usr/bin/python
# Copyright (c) PLUMgrid, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

from bcc import BPF
from sys import argv
from binascii import hexlify


b = BPF(text='int kprobe__sys_clone(void *ctx) { bpf_trace_printk("Hello, World! Here I did a sys_clone call!\\n"); return 0; }')

if len(argv) >= 2 and argv[1] == "--dump":
    print("Dump of kprobe__sys_clone:")
    g = b.dump_func('kprobe__sys_clone')
    for s in [g[i:i+8] for i in range(0, len(g), 8)]:
        print(hexlify(s))

b.trace_print()
