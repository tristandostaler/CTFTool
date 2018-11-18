#!/bin/bash -x

sudo locale-gen "en_US.UTF-8"

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
echo "LANG=en_US.UTF-8" | sudo tee /etc/default/locale > /dev/null
echo "LC_ALL=en_US.UTF-8" | sudo tee --append /etc/default/locale > /dev/null

cd $HOME
mkdir tools
cd tools

DEBIAN_FRONTEND=noninteractive
sudo -H rm -rf /var/lib/apt/lists/*

# Installing the 'apt-utils' package gets rid of the 'debconf: delaying package configuration, since apt-utils is not installed'
# error message when installing any other package with the apt package manager.
sudo -H apt update && sudo -H apt install -y --no-install-recommends \
    apt-utils \
    && sudo -H rm -rf /var/lib/apt/lists/*

sudo -H dpkg-reconfigure -u apt-utils

sudo -H apt update && sudo -H apt upgrade -y -o Dpkg::Options::="--force-confold"
sudo -H apt install -y aircrack-ng
sudo -H apt install -y autoconf
sudo -H apt install -y automake
sudo -H apt install -y autotools-dev
sudo -H apt install -y bison
sudo -H apt install -y bkhive
sudo -H apt install -y build-essential
sudo -H apt install -y clang
sudo -H apt install -y cmake
sudo -H apt install -y curl
sudo -H apt install -y dos2unix
sudo -H apt install -y dsniff
sudo -H apt install -y exif
sudo -H apt install -y exiv2
sudo -H apt install -y fcrackzip
sudo -H apt install -y foremost
sudo -H apt install -y g++
sudo -H apt install -y gcc
sudo -H apt install -y gdb
sudo -H apt install -y gdb-multiarch
sudo -H apt install -y gdbserver
sudo -H apt install -y git
sudo -H apt install -y imagemagick
sudo -H apt install -y libc6-arm64-cross
sudo -H apt install -y libc6-armhf-cross
sudo -H apt install -y libc6-dev-i386
sudo -H apt install -y libc6-i386
sudo -H apt install -y libcurl4-openssl-dev
sudo -H apt install -y libevent-dev
sudo -H apt install -y libffi-dev
sudo -H apt install -y libfreetype6
sudo -H apt install -y libfreetype6-dev
sudo -H apt install -y libglib2.0-dev
sudo -H apt install -y libgmp3-dev
sudo -H apt install -y libjpeg62-dev
sudo -H apt install -y libjpeg8
sudo -H apt install -y liblzma-dev
sudo -H apt install -y libmpc-dev
sudo -H apt install -y libmpfr-dev
sudo -H apt install -y libncurses5-dev
sudo -H apt install -y libncursesw5-dev
sudo -H apt install -y libpcap-dev
sudo -H apt install -y libreadline-dev
sudo -H apt install -y libsqlite3-dev
sudo -H apt install -y libssl-dev
sudo -H apt install -y libtool
sudo -H apt install -y libtool-bin
sudo -H apt install -y libxml2-dev
sudo -H apt install -y libxslt1-dev
sudo -H apt install -y llvm
sudo -H apt install -y lsb-release
sudo -H apt install -y masscan
sudo -H apt install -y most
sudo -H apt install -y nano
sudo -H apt install -y net-tools
sudo -H apt install -y nmap
sudo -H apt install -y ophcrack
sudo -H apt install -y outguess
sudo -H apt install -y pandoc
sudo -H apt install -y pngtools
sudo -H apt install -y python
sudo -H apt install -y python-dev
sudo -H apt install -y python-gmpy
sudo -H apt install -y python-imaging
sudo -H apt install -y python-magic
sudo -H apt install -y python-pip
sudo -H apt install -y python3-pip
sudo -H apt install -y python2.7
sudo -H apt install -y python3
sudo -H apt install -y samdump2
sudo -H apt install -y silversearcher-ag
sudo -H apt install -y socat
sudo -H apt install -y squashfs-tools
sudo -H apt install -y steghide
sudo -H apt install -y subversion
sudo -H apt install -y texinfo
sudo -H apt install -y tmux
sudo -H apt install -y tofrodos
sudo -H apt install -y tree
sudo -H apt install -y unzip
sudo -H apt install -y virtualenvwrapper
sudo -H apt install -y wamerican
sudo -H apt install -y wget
sudo -H apt install -y zlib1g-dev
sudo -H apt install -y zmap
sudo -H apt install -y libgmp-dev
sudo -H apt install -y libsqlite3-dev
sudo -H apt install -y 

# Install pwndbg
cd $HOME/tools
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh

sudo -H pip3 install --upgrade pip
sudo -H pip3 install --upgrade ipython
sudo -H pip install --upgrade angr
sudo -H pip3 install --upgrade pwntools

# Install radare2
cd $HOME/tools \
    && git clone https://github.com/radare/radare2 \
    && cd radare2 \
    && ./sys/install.sh \
    && sudo -H make symstall

# Install qemu
sudo -H apt install -y qemu qemu-user qemu-user-static
sudo -H apt install -y 'binfmt*'
sudo -H apt install -y libc6-armhf-armel-cross
sudo -H apt install -y debian-keyring
sudo -H apt install -y debian-archive-keyring
sudo -H apt update -m; echo 0 # Always success from update
sudo -H apt install -y libc6-mipsel-cross
sudo -H apt install -y libc6-armel-cross libc6-dev-armel-cross
sudo -H apt install -y libc6-armhf-cross libc6-dev-armhf-cross
sudo -H apt install -y binutils-arm-linux-gnueabi
sudo -H apt install -y libncurses5-dev
sudo -H mkdir /etc/qemu-binfmt
sudo -H ln -s /usr/mipsel-linux-gnu /etc/qemu-binfmt/mipsel
sudo -H ln -s /usr/arm-linux-gnueabihf /etc/qemu-binfmt/arm
sudo -H apt update

# Install binwalk
cd $HOME/tools \
    && git clone https://github.com/devttys0/binwalk \
    && cd binwalk \
    && sudo -H python3 setup.py install \

# Install firmware-mod-kit
cd $HOME/tools \
    && wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/firmware-mod-kit/fmk_099.tar.gz \
    && tar zxvf fmk_099.tar.gz \
    && rm fmk_099.tar.gz \
    && cd fmk/src \
    && ./configure \
    && make

# Install AFL with QEMU and clang-fast
cd $HOME/tools \
    && wget http://lcamtuf.coredump.cx/afl/releases/afl-latest.tgz \
    && tar -xzvf afl-latest.tgz \
    && rm afl-latest.tgz \
    && wget http://llvm.org/releases/3.8.0/clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz \
    && xz -d clang* \
    && tar xvf clang* \
    && cd clang* \
    && cd bin \
    && export PATH=$PWD:$PATH \
    && cd ../.. \
    && cd afl-* \
    && make \
    && cd llvm_mode \
    && make \
    && cd .. \
    && cd qemu* \
    && ./build_qemu_support.sh \
    && cd .. \
    && sudo -H make install \
    && cd $HOME/tools \
    && rm -rf clang*

sudo -H dpkg --add-architecture i386
sudo -H apt update
sudo -H apt install -y libc6:i386 libncurses5:i386 libstdc++6:i386 libc6-dev-i386

# Install apktool
sudo -H apt update \
    && sudo -H apt install -y default-jre \
    && wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool \
    && wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.0.2.jar \
    && sudo -H mv apktool_2.0.2.jar /bin/apktool.jar \
    && sudo -H mv apktool /bin/ \
    && sudo -H chmod 755 /bin/apktool \
    && sudo -H chmod 755 /bin/apktool.jar

# Install dotfiles
cd $HOME \
    && git clone https://github.com/tkk2112/dotfiles.git \
    && cd dotfiles \
    && ./install.sh

hash -r

# Install stegdetect/stegbreak
wget http://old-releases.ubuntu.com/ubuntu/pool/universe/s/stegdetect/stegdetect_0.6-6_amd64.deb \
    && sudo -H dpkg -i stegdetect_0.6-6_amd64.deb \
    && rm -rf stegdetect*

# Install John The Jumbo
cd $HOME/tools \
    && git clone --depth 1 https://github.com/magnumripper/JohnTheRipper.git \
    && cd JohnTheRipper/src \
    && ./configure \
    && sudo -H make -j2 install

# Install Pillow
sudo -H pip3 install --upgrade Pillow

# Install r2pipe
sudo -H pip3 install --upgrade r2pipe

# Install Frida
sudo -H pip3 install --upgrade frida

# Install ctf-tools
echo "export PATH=\$PATH:~/tools/ctf-tools/bin" >> $HOME/.bashrc
export PATH=$PATH:~/tools/ctf-tools/bin
cd $HOME/tools && git clone https://github.com/zardus/ctf-tools \
    && cd ctf-tools \
    && bin/manage-tools setup

$HOME/tools/ctf-tools/bin/manage-tools install subbrute
$HOME/tools/ctf-tools/bin/manage-tools install sqlmap
$HOME/tools/ctf-tools/bin/manage-tools install dirsearch
$HOME/tools/ctf-tools/bin/manage-tools install dirb
$HOME/tools/ctf-tools/bin/manage-tools install commix
$HOME/tools/ctf-tools/bin/manage-tools install burpsuite
$HOME/tools/ctf-tools/bin/manage-tools install exetractor
$HOME/tools/ctf-tools/bin/manage-tools install pdf-parser
$HOME/tools/ctf-tools/bin/manage-tools install peepdf
$HOME/tools/ctf-tools/bin/manage-tools install scrdec18
$HOME/tools/ctf-tools/bin/manage-tools install testdisk
$HOME/tools/ctf-tools/bin/manage-tools install cribdrag
$HOME/tools/ctf-tools/bin/manage-tools install foresight
$HOME/tools/ctf-tools/bin/manage-tools install featherduster
$HOME/tools/ctf-tools/bin/manage-tools install hashpump-partialhash
$HOME/tools/ctf-tools/bin/manage-tools install hash-identifier
$HOME/tools/ctf-tools/bin/manage-tools install littleblackbox
$HOME/tools/ctf-tools/bin/manage-tools install msieve
$HOME/tools/ctf-tools/bin/manage-tools install pemcrack
$HOME/tools/ctf-tools/bin/manage-tools install pkcrack
$HOME/tools/ctf-tools/bin/manage-tools install python-paddingoracle
$HOME/tools/ctf-tools/bin/manage-tools install reveng
$HOME/tools/ctf-tools/bin/manage-tools install sslsplit
$HOME/tools/ctf-tools/bin/manage-tools install xortool
$HOME/tools/ctf-tools/bin/manage-tools install yafu
$HOME/tools/ctf-tools/bin/manage-tools install elfkickers
$HOME/tools/ctf-tools/bin/manage-tools install xrop
$HOME/tools/ctf-tools/bin/manage-tools install evilize
$HOME/tools/ctf-tools/bin/manage-tools install checksec

# Install XSSer
sudo -H pip install --upgrade pycurl BeautifulSoup
cd $HOME/tools \
    && wget https://xsser.03c8.net/xsser/xsser_1.7-1_amd64.deb \
    && sudo -H dpkg -i xsser_1.7-1_amd64.deb \
    && rm -rf xsser*

# Install uncompyle2
cd $HOME/tools \
    && git clone https://github.com/wibiti/uncompyle2.git \
    && cd uncompyle2 \
    && sudo -H python setup.py install

sudo -H pip3 install --upgrade gmpy
sudo -H pip3 install --upgrade gmpy2
sudo -H pip3 install --upgrade numpy

# Install retdec decompiler
sudo -H pip3 install retdec-python

# https://blog.markvincze.com/download-artifacts-from-a-latest-github-release-in-sh-and-powershell/
cd $HOME/tools \
    && LATEST_RELEASE=$(curl -L -s -H 'Accept: application/json' https://github.com/radareorg/cutter/releases/latest) \
    && LATEST_VERSION=$(echo $LATEST_RELEASE | sed -e 's/.*"tag_name":"\([^"]*\)".*/\1/') \
    && ARTIFACT_URL="https://github.com/radareorg/cutter/releases/download/$LATEST_VERSION/Cutter-$LATEST_VERSION-x86_64.Linux.AppImage" \
    && wget $ARTIFACT_URL \
    && chmod +x Cutter-*-x86_64.Linux.AppImage


sudo reboot 0