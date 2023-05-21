# Dump of hello_world.py

# BPF bytecode

# eBPF bytecode

```
b7010000210a0000
6b1afcff00000000
b70100006f726c64
631af8ff00000000
1801000048656c6c
000000006f2c2057
7b1af0ff00000000
b701000000000000
731afeff00000000
bfa1000000000000
07010000f0ffffff
b70200000f000000
8500000006000000
b700000000000000
9500000000000000
```


# x86 instructions
My Hello World:

```
(gdb) disas /r  0xffffffffc0165d80, 0xffffffffc0165dfc
Dump of assembler code from 0xffffffffc0165d80 to 0xffffffffc0165dfc:
   0xffffffffc0165d80:  cc                              int3
   0xffffffffc0165d81:  cc                              int3
   0xffffffffc0165d82:  cc                              int3
   0xffffffffc0165d83:  cc                              int3
   0xffffffffc0165d84:  0f 1f 44 00 00                  nopl   0x0(%rax,%rax,1)
   0xffffffffc0165d89:  66 90                           xchg   %ax,%ax
   0xffffffffc0165d8b:  55                              push   %rbp
   0xffffffffc0165d8c:  48 89 e5                        mov    %rsp,%rbp
   0xffffffffc0165d8f:  48 81 ec 30 00 00 00            sub    $0x30,%rsp
   0xffffffffc0165d96:  bf 6c 21 0a 00                  mov    $0xa216c,%edi
   0xffffffffc0165d9b:  89 7d f8                        mov    %edi,-0x8(%rbp)
   0xffffffffc0165d9e:  48 bf 6c 6f 6e 65 20 63 61 6c   movabs $0x6c616320656e6f6c,%rdi
   0xffffffffc0165da8:  48 89 7d f0                     mov    %rdi,-0x10(%rbp)
   0xffffffffc0165dac:  48 bf 20 61 20 73 79 73 5f 63   movabs $0x635f737973206120,%rdi
   0xffffffffc0165db6:  48 89 7d e8                     mov    %rdi,-0x18(%rbp)
   0xffffffffc0165dba:  48 bf 72 65 20 49 20 64 69 64   movabs $0x6469642049206572,%rdi
   0xffffffffc0165dc4:  48 89 7d e0                     mov    %rdi,-0x20(%rbp)
   0xffffffffc0165dc8:  48 bf 6f 72 6c 64 21 20 48 65   movabs $0x65482021646c726f,%rdi
   0xffffffffc0165dd2:  48 89 7d d8                     mov    %rdi,-0x28(%rbp)
   0xffffffffc0165dd6:  48 bf 48 65 6c 6c 6f 2c 20 57   movabs $0x57202c6f6c6c6548,%rdi
   0xffffffffc0165de0:  48 89 7d d0                     mov    %rdi,-0x30(%rbp)
   0xffffffffc0165de4:  48 89 ef                        mov    %rbp,%rdi
   0xffffffffc0165de7:  48 83 c7 d0                     add    $0xffffffffffffffd0,%rdi
   0xffffffffc0165deb:  be 2c 00 00 00                  mov    $0x2c,%esi
   0xffffffffc0165df0:  e8 6b 4a ff c0                  callq  0xffffffff8115a860 <bpf_trace_printk>
   0xffffffffc0165df5:  31 c0                           xor    %eax,%eax
   0xffffffffc0165df7:  c9                              leaveq
   0xffffffffc0165df8:  c3                              retq
   0xffffffffc0165df9:  cc                              int3
   0xffffffffc0165dfa:  cc                              int3
   0xffffffffc0165dfb:  cc                              int3
```


Original hello world (prints "Hello World!\n")
```
   0xffffffffc01636dc:  cc      int3
   0xffffffffc01636dd:  cc      int3
   0xffffffffc01636de:  cc      int3
   0xffffffffc01636df:  cc      int3
   0xffffffffc01636e0:  0f 1f 44 00 00  nopl   0x0(%rax,%rax,1)
   0xffffffffc01636e5:  66 90   xchg   %ax,%ax
   0xffffffffc01636e7:  55      push   %rbp
   0xffffffffc01636e8:  48 89 e5        mov    %rsp,%rbp
   0xffffffffc01636eb:  48 81 ec 10 00 00 00    sub    $0x10,%rsp
   0xffffffffc01636f2:  bf 21 0a 00 00  mov    $0xa21,%edi
   0xffffffffc01636f7:  66 89 7d fc     mov    %di,-0x4(%rbp)
   0xffffffffc01636fb:  bf 6f 72 6c 64  mov    $0x646c726f,%edi
   0xffffffffc0163700:  89 7d f8        mov    %edi,-0x8(%rbp)
   0xffffffffc0163703:  48 bf 48 65 6c 6c 6f 2c 20 57   movabs $0x57202c6f6c6c6548,%rdi
   0xffffffffc016370d:  48 89 7d f0     mov    %rdi,-0x10(%rbp)
   0xffffffffc0163711:  31 ff   xor    %edi,%edi
   0xffffffffc0163713:  40 88 7d fe     mov    %dil,-0x2(%rbp)
   0xffffffffc0163717:  48 89 ef        mov    %rbp,%rdi
   0xffffffffc016371a:  48 83 c7 f0     add    $0xfffffffffffffff0,%rdi
   0xffffffffc016371e:  be 0f 00 00 00  mov    $0xf,%esi
   0xffffffffc0163723:  e8 38 71 ff c0  callq  0xffffffff8115a860 <bpf_trace_printk>
   0xffffffffc0163728:  31 c0   xor    %eax,%eax
   0xffffffffc016372a:  c9      leaveq
   0xffffffffc016372b:  c3      retq
   0xffffffffc016372c:  cc      int3
   0xffffffffc016372d:  cc      int3
   0xffffffffc016372e:  cc      int3
```
