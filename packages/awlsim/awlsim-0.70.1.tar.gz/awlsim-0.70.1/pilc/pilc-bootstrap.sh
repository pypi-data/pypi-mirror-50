#!/bin/sh
#
# PiLC bootstrap
#
# Copyright 2016-2019 Michael Buesch <m@bues.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

basedir="$(dirname "$0")"
[ "$(echo "$basedir" | cut -c1)" = '/' ] || basedir="$PWD/$basedir"

# The repository root is basedir.
basedir="$basedir/.."


MAIN_MIRROR="http://mirrordirector.raspbian.org/raspbian/"
DEFAULT_SUITE=stretch

PPL_VERSION="0.1.1"
PPL_FILE="ppl_v$PPL_VERSION.zip"
PPL_MIRROR="./libs/pixtend/v1/ppl/$PPL_FILE"
PPL_SHA256="103edcdbc377f8b478fcbc89117cbad143500c611cb714568f55513cece220d4"

PPL2_VERSION="0.1.3"
PPL2_FILE="pplv2_v$PPL2_VERSION.zip"
PPL2_MIRROR="./libs/pixtend/v2/pplv2/$PPL2_FILE"
PPL2_SHA256="cab6e7cd9062ffbf81a8f570ea0cad663addd8fe22e31cb75e887ae89e425651"


info()
{
	echo "--- $*"
}

error()
{
	echo "=== ERROR: $*" >&2
}

warning()
{
	echo "=== WARNING: $*" >&2
}

die()
{
	error "$*"
	exit 1
}

# print the first of its arguments.
first()
{
	echo "$1"
}

# print the last of its arguments.
last()
{
	while [ $# -gt 1 ]; do shift; done
	echo "$1"
}

# $1=program_name
have_program()
{
	which "$1" >/dev/null 2>&1
}

# $1=program_name, ($2=description)
assert_program()
{
	local bin="$1"
	local desc="$2"
	[ -n "$desc" ] || desc="$bin"
	have_program "$bin" || die "$bin not found. Please install $desc."
}

term_signal()
{
	die "Terminating signal received"
}

cleanup()
{
	info "Cleaning up..."
	for mp in "$mp_shm" "$mp_proc_binfmt_misc" "$mp_proc" "$mp_sys" "$mp_bootimgfile" "$mp_rootimgfile"; do
		[ -n "$mp" -a -d "$mp" ] &&\
			umount -l "$mp" >/dev/null 2>&1
	done
	for mp in "$mp_bootimgfile" "$mp_rootimgfile"; do
		[ -n "$mp" -a -d "$mp" ] &&\
			rmdir "$mp" >/dev/null 2>&1
	done
}

write_image()
{
	local image="$1"
	local dev="$2"

	[ -b "$dev" ] || die "$dev is not a block device"
	mount | grep -q "$dev" && die "$dev is mounted. Refusing to write to it!"

	if have_program blkdiscard; then
		info "Discarding $dev ..."
		blkdiscard "$dev" ||\
			error "blkdiscard failed."
	else
		warning "Skipping discard. blkdiscard not installed."
	fi

	info "Writing $image to $dev ..."

	dd if="$image" of="$dev" bs=32M status=progress ||\
		die "Failed to write image."
}

download()
{
	local target="$1"
	local mirror="$2"
	local sha256="$3"

	info "Downloading $mirror..."
	rm -f "$target"
	if printf '%s' "$mirror" | grep -qe '^\./'; then
		# "mirror" starts with ./
		# This is a local file in the repository.
		cp "$basedir/$mirror" "$target" || die "Failed to fetch $mirror"
	else
		# Download the file
		wget -O "$target" "$mirror" || die "Failed to fetch $mirror"
	fi
	[ "$(sha256sum -b "$target" | cut -f1 -d' ')" = "$sha256" ] ||\
		die "SHA256 verification of $target failed"
}

extract_archive()
{
	local archive="$1"
	local extract_dir="$2"
	local make_extract_dir="$3"

	if [ $make_extract_dir -ne 0 ]; then
		mkdir "$extract_dir" ||\
			die "Failed to create directory $extract_dir"
	fi
	if printf '%s' "$archive" | grep -qEe '\.zip$'; then
		if [ $make_extract_dir -ne 0 ]; then
			unzip -d "$extract_dir" "$archive" ||\
				die "Failed to unpack $archive"
		else
			unzip "$archive" ||\
				die "Failed to unpack $archive"
		fi
	else
		if [ $make_extract_dir -ne 0 ]; then
			tar --one-top-level="$extract_dir" -xf "$archive" ||\
				die "Failed to unpack $archive"
		else
			tar -xf "$archive" ||\
				die "Failed to unpack $archive"
		fi
	fi
}

build_pythonpack()
{
	local python="$1"
	local name="$2"
	local archive="$3"
	local extract_dir="$4"
	local make_extract_dir="$5"

	info "Building $name for $python..."
	rm -rf "/tmp/$extract_dir"
	(
		cd /tmp || die "Failed to cd /tmp"
		extract_archive "$archive" "$extract_dir" "$make_extract_dir"
		cd "$extract_dir" ||\
			die "Failed to cd $extract_dir"
		"$python" ./setup.py install ||\
			die "Failed to install $name"
	) || die
	rm -r "/tmp/$extract_dir" ||\
		die "Failed to remove $name build files."
}

build_ppl()
{
	local archive="$PPL_FILE"
	for python in python3; do
		build_pythonpack "$python" "ppl-$PPL_VERSION" \
				 "$archive" "ppl-$PPL_VERSION" 1
	done
	rm "/tmp/$archive" ||\
		die "Failed to remove /tmp/$archive."
}

build_ppl2()
{
	local archive="$PPL2_FILE"
	for python in python3; do
		build_pythonpack "$python" "ppl2-$PPL2_VERSION" \
				 "$archive" "ppl2-$PPL2_VERSION" 1
	done
	rm "/tmp/$archive" ||\
		die "Failed to remove /tmp/$archive."
}

pilc_bootstrap_first_stage()
{
	echo "Running first stage..."

	[ "$(id -u)" = "0" ] || die "Permission denied. Must be root."

	# Check host tools (first/third stage).
	assert_program debootstrap
	assert_program git
	assert_program chroot
	assert_program rsync
	assert_program parted
	assert_program mkfs.vfat
	assert_program mkfs.ext4
	assert_program 7z
	assert_program tar
	assert_program unzip
	assert_program install
	[ -x "$opt_qemu" ] ||\
		die "The qemu binary '$opt_qemu' is not executable."

	# debootstrap first stage.
	if [ $opt_skip_debootstrap1 -eq 0 ]; then
		info "Running debootstrap first stage..."
		debootstrap --arch="$opt_arch" --foreign --verbose \
			--keyring="$basedir_pilc/raspbian.public.key.gpg" \
			"$opt_suite" "$opt_target_dir" "$MAIN_MIRROR" \
			|| die "debootstrap failed"
		mkdir -p "$opt_target_dir/usr/share/keyrings" ||\
			die "Failed to create keyrings dir."
		cp "$basedir_pilc/raspbian.archive.public.key.gpg" \
		   "$opt_target_dir/usr/share/keyrings/" ||\
			die "Failed to copy raspbian.archive.public.key.gpg."
		cp /usr/share/keyrings/debian-archive-keyring.gpg \
		   "$opt_target_dir/usr/share/keyrings/debian-archive-keyring.gpg" ||\
			die "Failed to copy debian-archive-keyring.gpg."
	fi
	[ -d "$opt_target_dir" ] ||\
		die "Target directory '$opt_target_dir' does not exist."

	# Avoid the start of daemons during second stage.
	cp "$basedir_pilc/templates/policy-rc.d" "$opt_target_dir/usr/sbin/policy-rc.d" ||\
		die "Failed to create policy-rc.d"
	chmod 755 "$opt_target_dir/usr/sbin/policy-rc.d" ||\
		die "Failed to chmod policy-rc.d"

	info "Cleaning tmp..."
	rm -rf "$opt_target_dir"/tmp/*

	# Copy qemu.
	local qemu_bin="$opt_target_dir/$opt_qemu"
	if ! [ -x "$qemu_bin" ]; then
		info "Copying qemu binary from '$opt_qemu' to '$qemu_bin'..."
		mkdir -p "$(dirname "$qemu_bin")" ||\
			die "Failed to make qemu base directory."
		cp "$opt_qemu" "$qemu_bin" ||\
			die "Failed to copy qemu binary."
	fi

	info "Copying PiLC bootstrap script and templates..."
	cp "$basedir_pilc/pilc-bootstrap.sh" "$opt_target_dir/" ||\
		die "Failed to copy bootstrap script."
	cp -r "$basedir_pilc/templates" "$opt_target_dir/tmp/" ||\
		die "Failed to copy PiLC templates"

	info "Checking out awlsim..."
	local awlsim_dir="$opt_target_dir/tmp/awlsim"
	local checkout_dir="$awlsim_dir/src"
	rm -rf "$awlsim_dir"
	mkdir -p "$awlsim_dir" || die "mkdir failed"
	git clone --no-checkout "$basedir/.git" "$checkout_dir" ||\
		die "Failed to clone"
	(
		cd "$checkout_dir" ||\
			die "Failed to cd"
		git checkout "$opt_branch" ||\
			die "Failed to check out branch."
		git submodule update --init submodules/pyprofibus ||\
			die "Failed to pull pyprofibus submodule"
		rm -r .git submodules/pyprofibus/.git ||\
			die "Failed to remove .git directory."
		mv submodules/pyprofibus .. ||\
			die "Failed to move pyprofibus submodule."
	) || die

	# Fetch packages
	download "$opt_target_dir/tmp/$PPL_FILE" "$PPL_MIRROR" "$PPL_SHA256"
	download "$opt_target_dir/tmp/$PPL2_FILE" "$PPL2_MIRROR" "$PPL2_SHA256"

	# Second stage will mount a few filesystems.
	# Keep track to umount them in cleanup.
	mp_proc="$opt_target_dir/proc"
	mp_proc_binfmt_misc="$opt_target_dir/proc/sys/fs/binfmt_misc"
	mp_sys="$opt_target_dir/sys"
	mp_shm="$opt_target_dir/dev/shm"
}

pilc_bootstrap_second_stage()
{
	info "Running second stage ($opt_arch)..."

	[ -x /pilc-bootstrap.sh ] ||\
		die "Second stage does not contain the bootstrap script."

	# Set up environment.
	export LC_ALL=C
	export LANGUAGE=C
	export LANG=C
	if [ "$opt_rpiver" = "1" -o "$opt_rpiver" = "0" ]; then
		info "Optimizing for RPi 1.x, zero(w) or later"
		local march="armv6kz"
	elif [ "$opt_rpiver" = "2" ]; then
		info "Optimizing for RPi 2.x or later"
		local march="armv7-a"
	else
		info "Optimizing for RPi 3.x or later"
		local march="armv8-a"
	fi
	export CFLAGS="-O3 -march=$march -mfpu=vfp -mfloat-abi=hard -pipe"
	export CXXFLAGS="$CFLAGS"

	# debootstrap second stage.
	if [ $opt_skip_debootstrap2 -eq 0 ]; then
		info "Running debootstrap second stage..."
		/debootstrap/debootstrap --verbose --second-stage ||\
			die "Debootstrap second stage failed."
	fi

	info "Mounting /proc..."
	mkdir -p /proc ||\
		die "Failed to create /proc mountpoint."
	mount -t proc proc /proc ||\
		die "Mounting /proc failed."

	info "Mounting /sys..."
	mkdir -p /sys ||\
		die "Failed to create /sys mountpoint."
	mount -t sysfs sysfs /sys ||\
		die "Mounting /sys failed."

	info "Mounting /dev/shm..."
	mkdir -p /dev/shm ||\
		die "Failed to create /dev/shm mountpoint."
	mount -t tmpfs tmpfs /dev/shm ||\
		die "Mounting /dev/shm failed."

	info "Writing apt configuration..."
cat > /etc/apt/sources.list <<EOF
deb $MAIN_MIRROR $opt_suite main firmware rpi
deb http://archive.raspberrypi.org/debian/ $opt_suite main ui
EOF
	[ $? -eq 0 ] || die "Failed to set sources.list"
	echo 'Acquire { Languages "none"; };' > /etc/apt/apt.conf.d/99no-translations ||\
		die "Failed to set apt.conf.d"

	info "Creating /etc/fstab"
	mkdir -p /config ||\
		die "Failed to create /config"
	cp /tmp/templates/fstab /etc/fstab ||\
		die "Failed to create fstab"

	info "Writing misc /etc stuff..."
	echo "PiLC" > /etc/hostname ||\
		die "Failed to set hostname"
	printf 'PiLC GNU/Linux (based on Raspbian) \\n \\l\n\n' > /etc/issue ||\
		die "Failed to create /etc/issue"
	printf 'PiLC GNU/Linux (based on Raspbian)\n' > /etc/issue.net ||\
		die "Failed to create /etc/issue.net"
	sed -i -e 's|PRETTY_NAME=.*|PRETTY_NAME="PiLC"|' \
		/etc/os-release ||\
		die "Failed to set os-release PRETTY_NAME."
	sed -i -e 's|NAME=.*|NAME="PiLC"|' \
		/etc/os-release ||\
		die "Failed to set os-release NAME."
	sed -i -e 's|ID=.*|ID=pilc|' \
		/etc/os-release ||\
		die "Failed to set os-release ID."
	sed -i -e 's|ID_LIKE=.*|ID_LIKE=raspbian|' \
		/etc/os-release ||\
		die "Failed to set os-release ID_LIKE."
	sed -i -e 's|HOME_URL=.*|HOME_URL="https://bues.ch/a/pilc"|' \
		/etc/os-release ||\
		die "Failed to set os-release HOME_URL."
	sed -i -e 's|SUPPORT_URL=.*|SUPPORT_URL="https://bues.ch/a/pilc"|' \
		/etc/os-release ||\
		die "Failed to set os-release SUPPORT_URL."
	sed -i -e 's|BUG_REPORT_URL=.*|BUG_REPORT_URL="https://bues.ch/a/pilc"|' \
		/etc/os-release ||\
		die "Failed to set os-release BUG_REPORT_URL."

	info "Updating packages..."
	cat /tmp/templates/debconf-set-selections-preinstall.conf | debconf-set-selections ||\
		die "Failed to configure debconf settings"
	apt-key add /usr/share/keyrings/raspbian.archive.public.key.gpg ||\
		die "apt-key add failed"
	local apt_opts="-y -o Acquire::Retries=3"
	apt-get $apt_opts update ||\
		die "apt-get update failed"
	apt-get $apt_opts install apt-transport-https ||\
		die "apt-get install apt-transport-https failed"
	apt-get $apt_opts dist-upgrade ||\
		die "apt-get dist-upgrade failed"

	info "Installing packages..."
	apt-get $apt_opts install \
		aptitude \
		autoconf \
		automake \
		build-essential \
		console-setup \
		cython3 \
		dbus \
		debconf-utils \
		devscripts \
		firmware-brcm80211 \
		git \
		gnu-fdisk \
		htop \
		i2c-tools \
		irqbalance \
		iw \
		locales \
		nano \
		ntp \
		openssh-server \
		parted \
		pkg-config \
		python3 \
		python3-all-dev \
		python3-cffi \
		python3-coverage \
		python3-dev \
		python3-rpi.gpio \
		python3-serial \
		python3-setuptools \
		python3-spidev \
		quilt \
		raspberrypi-bootloader \
		raspi-config \
		raspi-copies-and-fills \
		raspi-gpio \
		rng-tools \
		schedtool \
		screen \
		sudo \
		systemd \
		tmux \
		vim \
		wireless-tools \
		wpasupplicant \
		|| die "apt-get install failed"

	info "Removing unnecessary packages..."
	apt-get $apt_opts purge \
		at \
		exim4-daemon-light \
		triggerhappy \
		|| die "apt-get purge failed"

	info "Configuring some packages..."
	cat /tmp/templates/debconf-set-selections-postinstall.conf | debconf-set-selections ||\
		die "Failed to configure debconf settings"
	dpkg-reconfigure -u locales ||\
		die "Failed to reconfigure locales"

	info "Cleaning apt..."
	apt-get $apt_opts autoremove --purge ||\
		die "apt-get autoremove failed"
	apt-get $apt_opts clean ||\
		die "apt-get clean failed"

	info "Disabling some services..."
	systemctl disable apt-daily.service ||\
		die "Failed to disable apt-daily.service"
	systemctl disable apt-daily.timer ||\
		die "Failed to disable apt-daily.timer"
	systemctl disable apt-daily-upgrade.timer ||\
		die "Failed to disable apt-daily-upgrade.timer"
	systemctl disable rsync.service ||\
		die "Failed to disable rsync.service"

	info "Building Python modules..."
	build_ppl
	build_ppl2

	info "Removing ssh keys..."
	cp /tmp/templates/regenerate_ssh_host_keys.sh \
		/etc/ssh/regenerate_ssh_host_keys.sh ||\
		die "Failed to copy regenerate_ssh_host_keys.sh"
	chmod 755 /etc/ssh/regenerate_ssh_host_keys.sh ||\
		die "Failed to chmod regenerate_ssh_host_keys.sh"
	cp /tmp/templates/regenerate_ssh_host_keys.service \
		/lib/systemd/system/regenerate_ssh_host_keys.service ||\
		die "Failed to copy regenerate_ssh_host_keys.service"
	systemctl enable regenerate_ssh_host_keys.service ||\
		die "Failed to enable regenerate_ssh_host_keys.service"
	systemctl disable ssh.service ||\
		die "Failed to disable ssh.service"
	if [ -e "$(first /etc/ssh/ssh_host_*_key*)" ]; then
		rm /etc/ssh/ssh_host_*_key* ||\
			die "Failed to remove ssh keys."
	fi
	echo 1 > /etc/ssh/sshd_not_to_be_run ||\
		die "Failed to create /etc/ssh/sshd_not_to_be_run"

	info "Creating /etc/rc.local..."
	cp /tmp/templates/rc.local /etc/rc.local ||\
		die "Failed to create /etc/rc.local"
	chmod 755 /etc/rc.local ||\
		die "Failed to chmod /etc/rc.local"

	info "Creating /etc/modules-load.d/i2c.conf..."
	cp /tmp/templates/modules-load-i2c.conf /etc/modules-load.d/i2c.conf ||\
		die "Failed to create /etc/modules-load.d/i2c.conf"

	info "Creating /etc/security/limits.d/pilc-limits.conf..."
	cp /tmp/templates/pilc-limits.conf /etc/security/limits.d/pilc-limits.conf ||\
		die "Failed to create pilc-limits.conf"

	info "Creating users/groups..."
	userdel -f pi
	groupdel pi
	rm -rf /home/pi
	groupadd -g 1000 pi ||\
		die "Failed to create group pi."
	useradd -u 1000 -d /home/pi -m -g pi\
		-G pi,lp,dialout,cdrom,floppy,audio,dip,src,video,plugdev,netdev,i2c\
		-s /bin/bash\
		pi ||\
		die "Failed to create user pi."
	printf 'raspberry\nraspberry\n' | passwd pi ||\
		die "Failed to set 'pi' password."
	cp /tmp/templates/sudoers-pi /etc/sudoers.d/00-pi ||\
		die "Failed to create /etc/sudoers.d/00-pi"

	info "Initializing home directory..."
	mkdir -p /home/pi/.vim || die "Failed to mkdir /home/pi/.vim"
	cp /tmp/templates/vimrc /home/pi/.vim/vimrc ||\
		die "Failed to create /home/pi/.vim/vimrc"
	cp /tmp/templates/tmux.conf /home/pi/.tmux.conf ||\
		die "Failed to create /home/pi/.tmux.conf"

	info "Building awlsim..."
	(
		cd /tmp/awlsim/src ||\
			die "Failed to cd"
		if [ $opt_cython -eq 0 ]; then
			# Disable cython
			sed -i -e '/Package: cython/,/^$/ d' \
				debian/control ||\
				die "Failed to patch control file (cython)"
			sed -i -e 's/export AWLSIM_CYTHON_BUILD=1/export AWLSIM_CYTHON_BUILD=0/' \
				debian/rules ||\
				die "Failed to patch rules file (cython)"
		fi
		# Disable pypy
		sed -i -e '/Package: pypy/,/^$/ d' -e '/^\s*pypy.*$/ d'\
			debian/control ||\
			die "Failed to patch control file (pypy)"
		sed -i -e 's/,pypy//' \
			debian/rules ||\
			die "Failed to patch rules file (pypy)"

		# Build the packages.
		debuild -uc -us -b -d || die "debuild failed"
		info "Built awlsim files:"
		ls .. || die "Failed to list results"

		info "Installing awlsim..."
		# Core
		dpkg -i ../python3-awlsim_*.deb ||\
			die "Failed to install python3-awlsim"
		if [ $opt_cython -ne 0 ]; then
			dpkg -i ../cython3-awlsim_*.deb ||\
				die "Failed to install cython3-awlsim"
		fi
		# hardware: dummy
		dpkg -i ../python3-awlsimhw-dummy_*.deb ||\
			die "Failed to install python3-awlsimhw-dummy"
		if [ $opt_cython -ne 0 ]; then
			dpkg -i ../cython3-awlsimhw-dummy_*.deb ||\
				die "Failed to install cython3-awlsimhw-dummy"
		fi
		# hardware: linuxcnc
		dpkg -i ../python3-awlsimhw-linuxcnc_*.deb ||\
			die "Failed to install python3-awlsimhw-linuxcnc"
		if [ $opt_cython -ne 0 ]; then
			dpkg -i ../cython3-awlsimhw-linuxcnc_*.deb ||\
				die "Failed to install cython3-awlsimhw-linuxcnc"
		fi
		# hardware: profibus
		dpkg -i ../python3-awlsimhw-profibus_*.deb ||\
			die "Failed to install python3-awlsimhw-profibus"
		if [ $opt_cython -ne 0 ]; then
			dpkg -i ../cython3-awlsimhw-profibus_*.deb ||\
				die "Failed to install cython3-awlsimhw-profibus"
		fi
		# hardware: RPi GPIO
		dpkg -i ../python3-awlsimhw-rpigpio_*.deb ||\
			die "Failed to install python3-awlsimhw-rpigpio"
		if [ $opt_cython -ne 0 ]; then
			dpkg -i ../cython3-awlsimhw-rpigpio_*.deb ||\
				die "Failed to install cython3-awlsimhw-rpigpio"
		fi
		# hardware: PiXtend
		dpkg -i ../python3-awlsimhw-pixtend_*.deb ||\
			die "Failed to install python3-awlsimhw-pixtend"
		if [ $opt_cython -ne 0 ]; then
			dpkg -i ../cython3-awlsimhw-pixtend_*.deb ||\
				die "Failed to install cython3-awlsimhw-pixtend"
		fi
		# Executables
		dpkg -i ../awlsim-server_*.deb ||\
			die "Failed to install awlsim-server"
		dpkg -i ../awlsim-client_*.deb ||\
			die "Failed to install awlsim-client"
		dpkg -i ../awlsim-symtab_*.deb ||\
			die "Failed to install awlsim-symtab"
		dpkg -i ../awlsim-test_*.deb ||\
			die "Failed to install awlsim-test"
		dpkg -i ../awlsim-proupgrade_*.deb ||\
			die "Failed to install awlsim-proupgrade"
		# Copy debs
		rm -rf /home/pi/deb/awlsim
		mkdir -p /home/pi/deb/awlsim ||\
			die "mkdir /home/pi/deb/awlsim failed"
		cp ../*awlsim*.deb ../*awlsim*.buildinfo ../*awlsim*.changes \
			/home/pi/deb/awlsim/ ||\
			die "Failed to copy awlsim debs"
		# Copy examples
		cp examples/EXAMPLE.awlpro /home/pi/generic-example.awlpro ||\
			die "Failed to copy EXAMPLE.awlpro."
		cp examples/raspberrypi-gpio.awlpro /home/pi/raspberrypi-gpio-example.awlpro ||\
			die "Failed to copy raspberrypi-gpio.awlpro."
		cp examples/raspberrypi-profibus.awlpro /home/pi/raspberrypi-profibus-example.awlpro ||\
			die "Failed to copy raspberrypi-profibus.awlpro."
		cp examples/raspberrypi-pixtend.awlpro /home/pi/raspberrypi-pixtend-example.awlpro ||\
			die "Failed to copy raspberrypi-pixtend.awlpro."

		#TODO run the testsuite

		# Install configuration
		mkdir -p /etc/awlsim || die "Failed to create /etc/awlsim"
		cp awlsimhw_pyprofibus.conf /etc/awlsim/ ||\
			die "Failed to copy awlsimhw_pyprofibus.conf"

		#TODO install unit via package
		info "Installing awlsim service unit..."
		local awlsim_prefix=/usr
		local pyver=3
		local site="$awlsim_prefix/lib/python$pyver/dist-packages"
		cat awlsim-server.service.in |\
		sed -e 's|@USER@|root|g' \
		    -e 's|@GROUP@|root|g' \
		    -e "s|@PREFIX@|$awlsim_prefix|g" \
		    -e 's|@WORKING_DIRECTORY@|/etc/awlsim|g' \
		    -e 's|@PROJECT@|/etc/awlsim/awlsim-server.awlpro|g' \
		    -e "s|@PYTHON@|/usr/bin/python$pyver|g" \
		    -e "s|@PYTHON_SITE@|$site|g" >\
		    /lib/systemd/system/awlsim-server.service ||\
		    die "Failed to create awlsim-server.service"
		systemctl enable awlsim-server.service ||\
			die "Failed to enable awlsim-server-service"
	) || die
	info "Building pyprofibus..."
	(
		cd /tmp/awlsim/pyprofibus ||\
			die "Failed to cd"
		if [ $opt_cython -eq 0 ]; then
			# Disable cython
			sed -i -e '/Package: cython/,/^$/ d' \
				debian/control ||\
				die "Failed to patch control file (cython)"
			sed -i -e 's/export PYPROFIBUS_CYTHON_BUILD=1/export PYPROFIBUS_CYTHON_BUILD=0/' \
				debian/rules ||\
				die "Failed to patch rules file (cython)"
		fi

		# Build the packages.
		debuild -uc -us -b -d || die "debuild failed"
		info "Built pyprofibus files:"
		ls .. || die "Failed to list results"

		info "Installing pyprofibus..."
		dpkg -i ../python3-pyprofibus_*.deb ||\
			die "Failed to install python3-pyprofibus"
		dpkg -i ../profisniff_*.deb ||\
			die "Failed to install profisniff"
		dpkg -i ../gsdparser_*.deb ||\
			die "Failed to install gsdparser"

		# Copy debs
		rm -rf /home/pi/deb/pyprofibus
		mkdir -p /home/pi/deb/pyprofibus ||\
			die "mkdir /home/pi/deb/pyprofibus failed"
		cp ../*pyprofibus*.deb ../*pyprofibus*.buildinfo ../*pyprofibus*.changes \
			../profisniff_*.deb ../gsdparser_*.deb \
			/home/pi/deb/pyprofibus/ ||\
			die "Failed to copy pyprofibus debs"
	) || die
	rm -r /tmp/awlsim ||\
		die "Failed to remove awlsim checkout."

	info "Configuring network..."
	cat > /etc/network/interfaces.d/lo <<EOF
auto lo
iface lo inet loopback
EOF
	[ $? -eq 0 ] || die "Failed to create /etc/network/interfaces.d/lo"
	cat > /etc/network/interfaces.d/enx <<EOF
allow-hotplug /enx*=enx
iface enx inet dhcp
iface enx inet6 auto
EOF
	[ $? -eq 0 ] || die "Failed to create /etc/network/interfaces.d/enx"
	cat > /etc/network/interfaces.d/eth <<EOF
allow-hotplug /eth*=eth
iface eth inet dhcp
iface eth inet6 auto
EOF
	[ $? -eq 0 ] || die "Failed to create /etc/network/interfaces.d/eth"
	for i in $(seq 0 9); do
		cat > /etc/network/interfaces.d/eth$i <<EOF
allow-hotplug eth$i
iface eth$i inet dhcp
iface eth$i inet6 auto
EOF
		[ $? -eq 0 ] || die "Failed to create /etc/network/interfaces.d/eth$i"
	done
	cat > /etc/network/interfaces.d/wlan0 <<EOF
#allow-hotplug wlan0
#iface wlan0 inet dhcp
#	wpa-ssid 'enter your SSID here'
#	wpa-psk 'enter your pre-shared-key (PSK) here'
#iface wlan0 inet6 auto
EOF
	[ $? -eq 0 ] || die "Failed to create /etc/network/interfaces.d/wlan0"

	info "Updating home directory permissions..."
	chown -R pi:pi /home/pi || die "Failed to change /home/pi permissions."

	# Remove rc.d policy file
	if [ -e /usr/sbin/policy-rc.d ]; then
		rm /usr/sbin/policy-rc.d ||\
			die "Failed to remove policy-rc.d"
	fi

	info "Stopping processes..."
	for i in dbus ssh irqbalance; do
		/etc/init.d/$i stop
	done
}

pilc_bootstrap_third_stage()
{
	info "Running third stage..."

	info "Umounting /dev/shm..."
	umount -l "$mp_shm" || die "Failed to umount /dev/shm"
	info "Umounting /sys..."
	umount -l "$mp_sys" || die "Failed to umount /sys"
	info "Umounting /proc/sys/fs/binfmt_misc..."
	umount -l "$mp_proc_binfmt_misc"
	info "Umounting /proc..."
	umount -l "$mp_proc" || die "Failed to umount /proc"

	info "Removing PiLC bootstrap script..."
	rm "$opt_target_dir/pilc-bootstrap.sh" ||\
		die "Failed to remove bootstrap script."

	info "Cleaning tmp..."
	rm -rf "$opt_target_dir"/tmp/*

	info "Configuring boot..."
	cp "$basedir_pilc/templates/boot_cmdline.txt" "$opt_target_dir/boot/cmdline.txt" ||\
		die "Failed to create /boot/cmdline.txt"
	cp "$basedir_pilc/templates/boot_config.txt" "$opt_target_dir/boot/config.txt" ||\
		die "Failed to create /boot/config.txt"
	local img="$(first "$opt_target_dir/boot/"vmlinuz-*-rpi)"
	if [ -e "$img" ]; then
		mv "$img" "$opt_target_dir/boot/kernel.img" ||\
			die "Failed to create kernel.img"
	fi
	local img="$(first "$opt_target_dir/boot/"initrd.img-*-rpi)"
	if [ -e "$img" ]; then
		mv "$img" "$opt_target_dir/boot/initrd.img" ||\
			die "Failed to create initrd.img"
	fi
	local img="$(first "$opt_target_dir/boot/"vmlinuz-*-rpi2)"
	if [ -e "$img" ]; then
		mv "$img" "$opt_target_dir/boot/kernel7.img" ||\
			die "Failed to create kernel7.img"
	fi
	local img="$(first "$opt_target_dir/boot/"initrd.img-*-rpi2)"
	if [ -e "$img" ]; then
		mv "$img" "$opt_target_dir/boot/initrd7.img" ||\
			die "Failed to create initrd7.img"
	fi

	# Prepare image paths.
	local imgfile="${opt_target_dir}${opt_imgsuffix}.img"
	local imgfile_zip="${imgfile}.7z"
	local bootimgfile="${imgfile}.boot"
	mp_bootimgfile="${bootimgfile}.mp"
	local rootimgfile="${imgfile}.root"
	mp_rootimgfile="${rootimgfile}.mp"
	rm -f "$imgfile" "$imgfile_zip" "$rootimgfile" "$bootimgfile"
	rmdir "$mp_bootimgfile" "$mp_rootimgfile" 2>/dev/null

	# Create images.
	if [ "$opt_img" -ne 0 ]; then
		# Calculate image size.
		local imgsize_b="$(expr "$opt_imgsize" \* 1000 \* 1000 \* 1000)"
		local imgsize_mib="$(expr "$imgsize_b" \/ 1024 \/ 1024)"
		# Reduce the size to make sure it fits every SD card.
		local imgsize_mib_red="$(expr \( "$imgsize_mib" \* 98 \) \/ 100)"
		[ -n "$imgsize_mib_red" ] || die "Failed to calculate image size"
		info "SD image size = $imgsize_mib_red MiB"

		info "Creating boot image..."
		mkfs.vfat -F 32 -i 7771B0BB -n boot -C "$bootimgfile" \
			$(expr \( 64 \* 1024 \) - \( 4 \* 1024 \) ) ||\
			die "Failed to create boot partition file system."
		mkdir "$mp_bootimgfile" ||\
			die "Failed to make boot partition mount point."
		mount -o loop "$bootimgfile" "$mp_bootimgfile" ||\
			die "Failed to mount boot partition."
		rsync -aHAX --inplace \
			"$opt_target_dir/boot/" "$mp_bootimgfile/" ||\
			die "Failed to copy boot files."
		umount "$mp_bootimgfile" ||\
			die "Failed to umount boot partition."
		rmdir "$mp_bootimgfile" ||\
			die "Failed to remove boot partition mount point."

		info "Creating root image..."
		mkfs.ext4 "$rootimgfile" $(expr \( "$imgsize_mib_red" - 64 \) \* 1024 ) ||\
			die "Failed to create root filesystem."
		mkdir "$mp_rootimgfile" ||\
			die "Failed to make root partition mount point."
		mount -o loop "$rootimgfile" "$mp_rootimgfile" ||\
			die "Failed to mount root partition."
		rsync -aHAX --inplace \
			--exclude='boot/*' \
			--exclude='proc/*' \
			--exclude='sys/*' \
			--exclude='dev/shm/*' \
			--exclude='tmp/*' \
			--exclude="$(basename "$opt_qemu")" \
			"$opt_target_dir/" "$mp_rootimgfile/" ||\
			die "Failed to copy root files."
		umount "$mp_rootimgfile" ||\
			die "Failed to umount root partition."
		rmdir "$mp_rootimgfile" ||\
			die "Failed to remove root partition mount point."

		info "Creating image '$imgfile'..."
		dd if=/dev/zero of="$imgfile" bs=1M count="$imgsize_mib_red" conv=sparse ||\
			die "Failed to create image file."
		parted "$imgfile" <<EOF
		    unit b
		    mklabel msdos
		    mkpart primary fat32 $(expr 4 \* 1024 \* 1024) $(expr 64 \* 1024 \* 1024 - 1)
		    mkpart primary ext4 $(expr 64 \* 1024 \* 1024) 100%
EOF
		[ $? -eq 0 ] || die "Failed to create partitions."

		info "Integrating boot image..."
		dd if="$bootimgfile" of="$imgfile"\
			seek=4 bs=1M conv=notrunc,sparse ||\
			die "Failed to integrate boot partition."
		rm "$bootimgfile" ||\
			die "Failed to delete boot partition image."

		info "Integrating root image..."
		dd if="$rootimgfile" of="$imgfile"\
			seek=64 bs=1M conv=notrunc,sparse ||\
			die "Failed to integrate root partition."
		rm "$rootimgfile" ||\
			die "Failed to delete root partition image."

		# Create zipped image.
		if [ "$opt_zimg" -ne 0 ]; then
			info "Compressing image..."
			7z -mx=9 a "$imgfile_zip" "$imgfile" ||\
				die "Failed to compress partition image."
		fi

		# Write the image to the SD card.
		if [ -n "$opt_writedev" ]; then
			write_image "$imgfile" "$opt_writedev"
		fi
	fi
}

usage()
{
	echo "pilc-bootstrap.sh [OPTIONS] TARGET_DIR"
	echo
	echo "Options:"
	echo
	echo " --branch|-b BRANCH      Select the awlsim branch or tag."
	echo "                         Default: $default_branch"
	echo
	echo " --no-cython|-C          Do not build Cython modules."
	echo "                         Default: Build cython modules"
	echo
	echo " --suite|-s SUITE        Select the suite."
	echo "                         Default: $default_suite"
	echo
	echo " --arch|-a ARCH          Select the default arch."
	echo "                         Default: $default_arch"
	echo
	echo " --qemu-bin|-Q PATH      Select qemu-user-static binary."
	echo "                         Default: $default_qemu"
	echo
	echo " --img-suffix|-X SUFFIX  Image file suffix."
	echo "                         Default: $default_imgsuffix"
	echo
	echo " --img-size|-S SIZEGB    Image file size, in Gigabytes (base 1000)."
	echo "                         Default: $default_imgsize"
	echo
	echo " --no-img|-I             Do not create an image."
	echo "                         Default: Create image."
	echo
	echo " --no-zimg|-Z            Do not create a 7zipped image."
	echo "                         Default: Create 7zipped image."
	echo
	echo " --write|-w DEV          Write image to an SD card after bootstrap."
	echo "                         DEV must be the /dev/mmcblkX path to the card."
	echo
	echo " --write-only|-W DEV     Write an existing image to an SD card"
	echo "                         without bootstrap and image generation."
	echo
	echo " --skip-debootstrap1|-1  Skip debootstrap first stage."
	echo " --skip-debootstrap2|-2  Skip debootstrap second stage."
	echo
	echo " --quick|-q              Quick build. This is a shortcut for:"
	echo "                         --no-cython --no-zimg"
	echo
	echo " --rpiver|-R VERSION     Minimum Raspberry Pi version to build for."
	echo "                         Can be either 0, 1, 2 or 3."
	echo "                         0 and 1 are equivalent."
	echo "                         Default: 1"
}

# canonicalize basedir
basedir="$(readlink -e "$basedir")"
[ -n "$basedir" ] || die "Failed to canonicalize base directory."

# Directory containing the PiLC bootstrapping files.
basedir_pilc="$basedir/pilc"

# Mountpoints. Will be umounted on cleanup.
mp_shm=
mp_proc=
mp_proc_binfmt_misc=
mp_sys=
mp_bootimgfile=
mp_rootimgfile=

trap term_signal TERM INT

if [ -z "$__PILC_BOOTSTRAP_SECOND_STAGE__" ]; then
	# First stage

	export _NPROCESSORS_ONLN="$(getconf _NPROCESSORS_ONLN)"
	[ -n "$_NPROCESSORS_ONLN" ] || die "Failed to get # of online CPUs"

	default_branch="master"
	default_suite="$DEFAULT_SUITE"
	default_arch="armhf"
	default_qemu="/usr/bin/qemu-arm-static"
	default_imgsuffix="-$(date '+%Y%m%d')"
	default_imgsize=4
	default_img=1
	default_zimg=1
	default_writedev=
	default_writeonly=0
	default_rpiver=1

	opt_target_dir=
	opt_branch="$default_branch"
	opt_cython=1
	opt_suite="$default_suite"
	opt_arch="$default_arch"
	opt_qemu="$default_qemu"
	opt_skip_debootstrap1=0
	opt_skip_debootstrap2=0
	opt_imgsuffix="$default_imgsuffix"
	opt_imgsize="$default_imgsize"
	opt_img="$default_img"
	opt_zimg="$default_zimg"
	opt_writedev="$default_writedev"
	opt_writeonly="$default_writeonly"
	opt_rpiver="$default_rpiver"

	while [ $# -ge 1 ]; do
		case "$1" in
		--help|-h)
			usage
			exit 0
			;;
		--branch|-b)
			shift
			opt_branch="$1"
			[ -n "$opt_branch" ] || die "No branch given"
			;;
		--no-cython|-C)
			opt_cython=0
			;;
		--suite|-s)
			shift
			opt_suite="$1"
			[ -n "$opt_suite" ] || die "No suite given"
			;;
		--arch|-a)
			shift
			opt_arch="$1"
			[ -n "$opt_arch" ] || die "No arch given"
			;;
		--qemu-bin|-Q)
			shift
			opt_qemu="$1"
			[ -x "$opt_qemu" ] || die "No valid qemu binary given"
			;;
		--skip-debootstrap1|-1)
			opt_skip_debootstrap1=1
			;;
		--skip-debootstrap2|-2)
			opt_skip_debootstrap2=1
			;;
		--img-suffix|-X)
			shift
			opt_imgsuffix="$1"
			;;
		--img-size|-S)
			shift
			opt_imgsize="$(expr "$1" \* 1)"
			[ -n "$opt_imgsize" ] || die "--img-size|-S is invalid"
			;;
		--no-zimg|-Z)
			opt_zimg=0
			;;
		--no-img|-I)
			opt_img=0
			;;
		--quick|-q)
			opt_cython=0
			opt_zimg=0
			;;
		--write|-w|--write-only|-W)
			if [ "$1" = "--write" -o "$1" = "-w" ]; then
				opt_writeonly=0
			else
				opt_writeonly=1
			fi
			shift
			opt_writedev="$1"
			[ -b "$opt_writedev" ] || die "Invalid SD card block device"
			;;
		--rpiver|-R)
			shift
			opt_rpiver="$1"
			[ "$opt_rpiver" = "0" -o\
			  "$opt_rpiver" = "1" -o\
			  "$opt_rpiver" = "2" -o\
			  "$opt_rpiver" = "3" ] || die "Invalid --rpiver|-R"
			;;
		*)
			opt_target_dir="$*"
			break
			;;
		esac
		shift
	done
	[ -n "$opt_target_dir" ] ||\
		die "No TARGET_DIR"
	opt_target_dir="$(readlink -m "${opt_target_dir}")"
	[ -n "$opt_target_dir" ] || die "Failed to resolve target dir."
	[ -d "$opt_target_dir" -o ! -e "$opt_target_dir" ] ||\
		die "$opt_target_dir is not a directory"

	trap cleanup EXIT

	if [ -n "$opt_writedev" -a $opt_writeonly -ne 0 ]; then
		# Just write the image to the SD card, then exit.
		write_image "${opt_target_dir}${opt_imgsuffix}.img" "$opt_writedev"
		exit 0
	fi

	# Run first stage.
	pilc_bootstrap_first_stage

	info "Starting second stage."
	# Export options for use by second stage.
	export opt_target_dir
	export opt_branch
	export opt_cython
	export opt_suite
	export opt_arch
	export opt_qemu
	export opt_skip_debootstrap1
	export opt_skip_debootstrap2
	export opt_imgsuffix
	export opt_zimg
	export opt_img
	export opt_writedev
	export opt_writeonly
	export opt_rpiver
	export __PILC_BOOTSTRAP_SECOND_STAGE__=1
	chroot "$opt_target_dir" "/pilc-bootstrap.sh" ||\
		die "Chroot failed."

	# Run third stage.
	pilc_bootstrap_third_stage

	info ""
	info "Successfully bootstrapped PiLC."

	exit 0
else
	# Run second stage
	pilc_bootstrap_second_stage

	exit 0
fi
