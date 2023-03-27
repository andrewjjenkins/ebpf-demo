1. Install rasbpi (debian) image to SD card:

https://raspi.debian.net/tested-images/

This is tested on a Raspberry Pi 4 version B.  It should work on any of the
Raspberry Pi systems where the CPU and raspi are 64-bit, which is everything
Raspberry Pi 3 and later.

Your SD card must be at least 8GB.

I used https://raspi.debian.net/tested/20230102_raspi_4_bullseye.img.xz , which
was the most recent from the bullseye release for raspi 4 at the time of writing.


2. Do initial headless setup (optional)

You can either connect a monitor and keyboard and do initial setup that way, or
you can bootstrap so you can do it over the network.  This step describes how to
bootstrap it.  You will need a wired network connection.

You need to edit the file `sysconf.txt` on the `RASPIFIRM` volume on the SD card.

If you can't find the `RASPIFIRM` volume, you may need to eject and re-insert
the SD card to get your host operating system to re-read the card and mount the
RASPIFIRM volume.

Set the hostname and root_pw fields, below are examples.

```
root_pw=changeme
hostname=ebpf-pi
```

3. Boot Raspberry Pi

Put the SD card into the raspberry pi and boot it.  The first boot may take a
minute or so.  You need to find the IP address of the raspberry pi; you may be
able to do this via your router.

SSH into the raspberry pi, using the password you configured:

```
ssh root@<ip-address>
Password: changeme
root@ebpf-pi:~#
```

4. Initial setup

I add a non-root user `andrew` below; feel free to replace with whatever
username you'd like. I also install some utilities, this is optional but I find
linux unliveable without them.

```
apt-get update
apt-get dist-upgrade -y
apt-get install sudo git build-essential lm-sensors
# The remaining lines are optional
apt-get install vim tmux direnv bash-completion htop
adduser andrew 
passwd andrew
  <set any password you want>
adduser andrew sudo
```

The dist-upgrade probably installed a new kernel for you.  You should reboot
before we bother trying to build bcc.

```
reboot
```

The rest of the instructions will assume you are logged in as the non-root user
(`andrew` in my example), and will use sudo when needed.  If you didn't make a
non-root user and you're doing everything as root, the extra sudo in the
commands below won't hurt.

5. Build a kernel

```
echo "deb-src http://deb.debian.org/debian bullseye main non-free" | sudo tee -a /etc/apt/sources.list
echo "deb-src http://deb.debian.org/debian bullseye-updates main non-free" | sudo tee -a /etc/apt/sources.list
echo "deb-src http://security.debian.org/debian-security bullseye-security main non-free" | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install fakeroot
sudo apt-get build-dep linux
```


5. Install BCC compile-time dependencies

```
sudo apt-get install arping bison clang-format cmake dh-python \
  dpkg-dev pkg-kde-tools ethtool flex inetutils-ping iperf \
  libbpf-dev libclang-dev libclang-cpp-dev libedit-dev libelf-dev \
  libfl-dev libzip-dev linux-libc-dev llvm-dev libluajit-5.1-dev \
  luajit python3-netaddr python3-pyroute2 python3-distutils python3 \
  liblzma-dev libdebuginfod-dev zip linux-headers-$(uname -r)
```

6. Build BCC

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
-- The C compiler identification is GNU 10.2.1
-- The CXX compiler identification is GNU 10.2.1
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
Submodule 'libbpf-tools/blazesym' (https://github.com/libbpf/blazesym) registered for path 'libbpf-tools/blazesym'
Cloning into '/home/andrew/ebpf/bcc/libbpf-tools/blazesym'...
Warning: Permanently added the ECDSA host key for IP address '140.82.113.3' to the list of known hosts.
Submodule path 'libbpf-tools/blazesym': checked out 'd954f73867527dc75025802160c759d0b6a0641f'
Submodule 'libbpf-tools/bpftool' (https://github.com/libbpf/bpftool) registered for path 'libbpf-tools/bpftool'
Submodule 'src/cc/libbpf' (https://github.com/libbpf/libbpf.git) registered for path 'src/cc/libbpf'
Cloning into '/home/andrew/ebpf/bcc/libbpf-tools/bpftool'...
Cloning into '/home/andrew/ebpf/bcc/src/cc/libbpf'...
Submodule path 'libbpf-tools/bpftool': checked out '6eb3e20583da834da18ea3011dcefd08b3493f8d'
Submodule 'libbpf' (https://github.com/libbpf/libbpf.git) registered for path 'libbpf-tools/bpftool/libbpf'
Cloning into '/home/andrew/ebpf/bcc/libbpf-tools/bpftool/libbpf'...
Submodule path 'libbpf-tools/bpftool/libbpf': checked out '7984737fbf3b2a14a86321387bb62abb16cfc4ed'
Submodule path 'src/cc/libbpf': checked out 'ea284299025bf85b85b4923191de6463cd43ccd6'
-- Latest recognized Git tag is v0.26.0
-- Git HEAD is 594ab9a9b0e3dfa7cf8fc7f28923ba0eb33a5c66
-- Revision is 0.26.0+594ab9a9 (major 0, minor 26, patch 0)
-- Performing Test HAVE_NO_PIE_FLAG
-- Performing Test HAVE_NO_PIE_FLAG - Success
-- Performing Test HAVE_REALLOCARRAY_SUPPORT
-- Performing Test HAVE_REALLOCARRAY_SUPPORT - Success
-- Kernel release: 5.10.0-21-arm64
-- Kernel headers: KERNELHEADERS_DIR-NOTFOUND
-- Found LLVM: /usr/lib/llvm-11/include 11.0.1 (Use LLVM_ROOT envronment variable for another version of LLVM)
-- Found BISON: /usr/bin/bison (found version "3.7.5")
-- Found FLEX: /usr/bin/flex (found version "2.6.4")
-- Found LibElf: /usr/lib/aarch64-linux-gnu/libelf.so
-- Performing Test ELF_GETSHDRSTRNDX
-- Performing Test ELF_GETSHDRSTRNDX - Success
-- Found LibDebuginfod: /usr/lib/aarch64-linux-gnu/libdebuginfod.so
-- Found LibLzma: /usr/lib/aarch64-linux-gnu/liblzma.so
-- Using static-libstdc++
-- Found LuaJIT: /usr/lib/aarch64-linux-gnu/libluajit-5.1.a;/usr/lib/aarch64-linux-gnu/libdl.so;/usr/lib/aarch64-linux-gnu/libm.so
CMake Warning at tests/python/CMakeLists.txt:10 (message):
  Recommended test program 'netperf' not found


-- Configuring done
-- Generating done
-- Build files have been written to: /home/andrew/ebpf/bcc/build
```

The `make` step takes about 10 minutes or so on a Raspberry Pi 4.

7. Test BCC

Test that everything is working by running an example.

Once you start `HelloWorld`, your system needs to start another process for
anything to actually happen (something in the system needs to use the
`sys_clone` call).  You can wait a few seconds and see if you get lucky, and
some background daemon starts a process, or you can create one (ssh in again, or
make a new terminal if you are in tmux).

```
sudo examples/cpp/HelloWorld
```

8. Install prometheus, grafana, node-exporter

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


