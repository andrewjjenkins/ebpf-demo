#!/usr/bin/env python
#
# forktop Count which processes are forking the most.
#
# USAGE: forktop
#
# This is based on pidpersec.py (from bcc/examples)
#
# Copyright (c) 2023 Andrew Jenkins
# Licensed under the Apache License, Version 2.0 (the "License")

from bcc import BPF
from time import sleep, strftime

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

BPF_HASH(forks);

int kprobe__sched_fork(
    struct pt_regs *ctx,
    unsigned long clone_flags,
    struct task_struct *p)
{
    forks.increment((p->pid));
    return 0;
}
""")

# Python code: a big loop that reads the eBPF outputs:
#   - forks: A BPF_HASH() table
#   - trace_readline: Any BPF calls to bpf_trace_printk (for debugging)
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
