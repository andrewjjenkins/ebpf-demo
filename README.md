
# Introduction

This is the source code for a demo of eBPF.

The demo is based around a performance problem that is difficult to diagnose
with many traditional performance/monitoring tools.  We use eBPF and BCC (a
toolchain for eBPF) to diagnose it.

# Setup

## Pre-requisites

You will need a linux system with about 22GiB of disk space, 4 GB of memory, 2
CPUs.  A VM is great.

These instructions are tested on `amd64`; eBPF works on other architectures but
there are some differences in which hooks are exposed.  I believe this demo
works on other architectures but have not tried.

You need a linux system running a relatively recent kernel with eBPF enabled.  I
tested Ubuntu 22.04, but Ubuntu 20.04 is probably fine.  
Not all kernels enable eBPF; one way to check is to grep the kernel config for
BPF.

```
grep "BPF" /lib/modules/$(uname -r)/build/.config

# If that doesn't work, try this.  "modprobe configs" may or may not be
# required; if it fails, try checking the /proc/config.gz file anyway
modprobe configs
cat /proc/config.gz | gunzip | grep "BPF"
```

For this demo, you'll need `CONFIG_BPF`, `CONFIG_HAVE_EBPF_JIT`,
`CONFIG_BPF_JIT`, `CONFIG_BPF_SYSCALL`, `CONFIG_BPF_EVENTS`.  Here's the output on my demo system:

```
CONFIG_BPF=y
CONFIG_HAVE_EBPF_JIT=y
CONFIG_ARCH_WANT_DEFAULT_BPF_JIT=y
# BPF subsystem
CONFIG_BPF_SYSCALL=y
CONFIG_BPF_JIT=y
CONFIG_BPF_JIT_ALWAYS_ON=y
CONFIG_BPF_JIT_DEFAULT_ON=y
CONFIG_BPF_UNPRIV_DEFAULT_OFF=y
# CONFIG_BPF_PRELOAD is not set
CONFIG_BPF_LSM=y
# end of BPF subsystem
CONFIG_CGROUP_BPF=y
CONFIG_IPV6_SEG6_BPF=y
CONFIG_NETFILTER_XT_MATCH_BPF=m
CONFIG_BPFILTER=y
CONFIG_BPFILTER_UMH=m
CONFIG_NET_CLS_BPF=m
CONFIG_NET_ACT_BPF=m
CONFIG_BPF_STREAM_PARSER=y
CONFIG_LWTUNNEL_BPF=y
CONFIG_BPF_EVENTS=y
CONFIG_BPF_KPROBE_OVERRIDE=y
CONFIG_TEST_BPF=m
```

## Install BCC from source

Install all the dependencies to build BCC:

```
sudo apt-get install arping bison clang-format cmake dh-python \
  dpkg-dev pkg-kde-tools ethtool flex inetutils-ping iperf \
  libbpf-dev libclang-dev libclang-cpp-dev libedit-dev libelf-dev \
  libfl-dev libzip-dev linux-libc-dev llvm-dev libluajit-5.1-dev \
  luajit python3-netaddr python3-pyroute2 python3-distutils python3 \
  liblzma-dev libdebuginfod-dev zip linux-headers-$(uname -r)
```

```
git clone git@github.com:iovisor/bcc.git
mkdir -p bcc/build
pushd bcc/build
cmake ..
make
sudo make install
```

Example good "cmake" output below.  netperf is not readily available on debian
due to licensing, but it's only needed for some examples.  For the rest, you
should be looking for a lot of "Success" and no errors.

```
$ cmake ..
-- The C compiler identification is GNU 11.3.0
-- The CXX compiler identification is GNU 11.3.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Latest recognized Git tag is v0.26.0
-- Git HEAD is 594ab9a9b0e3dfa7cf8fc7f28923ba0eb33a5c66
-- Revision is 0.26.0+594ab9a9 (major 0, minor 26, patch 0)
-- Performing Test HAVE_NO_PIE_FLAG
-- Performing Test HAVE_NO_PIE_FLAG - Success
-- Performing Test HAVE_REALLOCARRAY_SUPPORT
-- Performing Test HAVE_REALLOCARRAY_SUPPORT - Success
-- Kernel release: 5.15.0-69-generic
-- Kernel headers: /usr/src/linux-headers-5.15.0-69-generic
-- Performing Test HAVE_FFI_CALL
-- Performing Test HAVE_FFI_CALL - Success
-- Found FFI: /usr/lib/x86_64-linux-gnu/libffi.so
-- Performing Test Terminfo_LINKABLE
-- Performing Test Terminfo_LINKABLE - Success
-- Found Terminfo: /usr/lib/x86_64-linux-gnu/libtinfo.so
-- Found ZLIB: /usr/lib/x86_64-linux-gnu/libz.so (found version "1.2.11")
-- Found LibXml2: /usr/lib/x86_64-linux-gnu/libxml2.so (found version "2.9.13")
-- Found LLVM: /usr/lib/llvm-14/include 14.0.0 (Use LLVM_ROOT envronment variable for another version of LLVM)
-- Found BISON: /usr/bin/bison (found version "3.8.2")
-- Found FLEX: /usr/bin/flex (found version "2.6.4")
-- Found LibElf: /usr/lib/x86_64-linux-gnu/libelf.so
-- Performing Test ELF_GETSHDRSTRNDX
-- Performing Test ELF_GETSHDRSTRNDX - Success
-- Found LibDebuginfod: /usr/lib/x86_64-linux-gnu/libdebuginfod.so
-- Found LibLzma: /usr/lib/x86_64-linux-gnu/liblzma.so
-- Using static-libstdc++
-- Found LuaJIT: /usr/lib/x86_64-linux-gnu/libluajit-5.1.a;/usr/lib/x86_64-linux-gnu/libdl.a;/usr/lib/x86_64-linux-gnu/libm.so
CMake Warning at tests/python/CMakeLists.txt:10 (message):
  Recommended test program 'netperf' not found


-- Configuring done
-- Generating done
-- Build files have been written to: /home/andrew/ebpf/bcc/build
```

The `make` step may take a few minutes.

## Test BCC

Test that everything is working by running an example.

Once you start `HelloWorld`, your system needs to start another process for
anything to actually happen (something in the system needs to use the
`sys_clone` call).  You can wait a few seconds and see if you get lucky, and
some background daemon starts a process, or you can create one (ssh in again, or
make a new terminal if you are in tmux).

```
sudo examples/cpp/HelloWorld
```

## Install prometheus, grafana, node-exporter

```
sudo snap install prometheus
sudo snap install --beta node-exporter
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_9.4.7_amd64.deb
sudo dpkg -i grafana_9.4.7_amd64.deb
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable grafana-server
```

Go to http://localhost:3000 and sign in as "admin" / "admin".  If it forces you
to choose a new password, you can, or you can just enter "admin" again.

Go to settings -> data sources, add Prometheus.  Server name is `http://localhost:9090`.

Go to Dashboards -> Import, and import ID# `1860`.  Set the Data Source to "Prometheus" and import.

## Install demo tools

```
sudo apt-get install htop hey nginx
```

## Build badly-performing app
In this directory:

```
make
```

# Demo

## Happy state

Open http://localhost:3000 , sign in (admin/admin), then go to the Node Exporter
Full dashboard.  Set the timeframe to "Last 15 minutes" and the refresh rate to
"10s" (top-right).

Start `htop`:

```
htop
```

In another terminal, start `hey` loading down NGINX.  You want the total load to
in htop to be about 50% (adjust `-q`; somewhere between 30% and 70% is fine, it
may bounce around).

```
hey -n 1000000000000 -cpus 2 -q 80 http://localhost
```

This represents a happy web server.  It's not fully loaded, but it's not idle.
The top processes in htop are probably `hey` and `nginx: worker process`.

![Screenshot of htop, showing hey and nginx and about 50% load](/images/happy-server-htop.gif)

In Grafana, you can see 50% of CPU being consumed:

![Screenshot of grafana, showing about 50% load](/images/happy-server-grafana.gif)



## Start what?

Now let's start the unknown perf-killing process.

