#!/usr/bin/env python3
#
# trip_verifier.py will not be accepted by the BPF verifier
#
# You should get an error:
# The sequence of 8193 jumps is too complex.
# processed 98324 insns (limit 1000000) max_states_per_insn 4 total_states 1029 peak_states 1029 mark_read 2
#
# If you fix that error (try switching the for loop with the commented one)
# and uncomment the bpf_trace_printk, you will get this error:
# value -2147483648 makes fp pointer be out of bounds
# processed 27 insns (limit 1000000) max_states_per_insn 0 total_states 0 peak_states 0 mark_read 0
#
#
# Copyright (c) 2023 Andrew Jenkins
# Licensed under the Apache License, Version 2.0 (the "License")


from bcc import BPF
from time import sleep, strftime
from itertools import islice
from binascii import hexlify
from sys import argv

b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/iocontext.h>

BPF_HASH(forks);

int kprobe__sched_fork(
    struct pt_regs *ctx,
    unsigned long clone_flags,
    struct task_struct *p)
{
    char mystring[4] = {'h', 'i', '!', '\\0' };

    // Try changing the line below to (uncomment):
    // for (unsigned int i = 40; i > 0; i -= 1) {
    for (unsigned int i = p->pid; i > 0; i -= 47) {
        forks.increment((p->pid));
    }

    // Try uncommenting the below:
    // bpf_trace_printk("The pid'th entry in mystring is: %d", mystring[p->pid]);
    return 0;
}
""")

if len(argv) >= 2 and argv[1] == "--dump":
    print("Dump of kprobe__sched_fork:")
    g = b.dump_func('kprobe__sched_fork')
    for s in [g[i:i+8] for i in range(0, len(g), 8)]:
        print(hexlify(s))

while (1):
    try:
        sleep(1)
    except KeyboardInterrupt:
        exit()

    print("%s: Top forkers last second:" % (strftime("%H:%M:%S")))
    for parent, count in sorted(b["forks"].items(), key=lambda x: x[1].value):
        if (count.value < 1):
            continue
        processName = parent.value
        try:
            cmdline = open("/proc/%d/cmdline" % parent.value, "r").read()
            if len(cmdline) > 40:
                cmdline = cmdline[0:40] + "..."
            processName = "%s (%d)" % (cmdline, parent.value)
        except:
            pass
        print("  parent %s: %d forks" % (processName, count.value))
    b["forks"].clear()

    # Print any calls to bpf_trace_printk
    while (1):
        line = b.trace_readline(nonblocking=True)
        if line is None or len(line) == 0:
            break
        print(line)
