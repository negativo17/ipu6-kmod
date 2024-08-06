# ipu6-drivers
%global commit0 9369b88ec1ea03670fb2dbfe7abdff411683d462
%global date 20240719
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
# ivsc-driver
%global commit1 b5969f9311c07a80250c3ab5e1174a792195e8e3
%global date 20240514
%global shortcommit1 %(c=%{commit0}; echo ${c:0:7})

# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:       ipu6-kmod
Version:    0
Release:    8.%{date}git%{shortcommit0}%{?dist}
Summary:    Kernel drivers for the IPU 6 and sensors
License:    GPL-3.0-only
URL:        https://github.com/intel/ipu6-drivers

Source0:    https://github.com/intel/ipu6-drivers/archive/%{commit0}.tar.gz#/ipu6-drivers-%{shortcommit0}.tar.gz
Source1:    https://github.com/intel/ivsc-driver/archive/%{commit1}.tar.gz#/ivsc-driver-%{shortcommit1}.tar.gz
Source2:    intel-vsc-fw.patch
# https://github.com/intel/ipu6-drivers/pull/214
Patch0:     214.patch
# https://github.com/intel/ipu6-drivers/pull/239
Patch1:     239.patch
# https://github.com/intel/ipu6-drivers/pull/242
Patch2:     242.patch
# https://github.com/intel/ipu6-drivers/pull/243
Patch3:     243.patch
# https://github.com/jwrdegoede/ipu6-drivers/commit/2c4ad1398dddfb307e8a40a714a6d5f70d6d14cb
Patch4:     2c4ad1398dddfb307e8a40a714a6d5f70d6d14cb.patch

# Get the needed BuildRequires (in parts depending on what we build for):
BuildRequires:  kmodtool

# kmodtool does its magic here:
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Kernel drivers for the VSC, IPU 6 and sensors. It supports MIPI cameras through
the IPU6 on Intel Tiger Lake, Alder Lake, Raptor Lake and Meteor Lake platforms.

%prep
# Error out if there was something wrong with kmodtool:
%{?kmodtool_check}
# Print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p1 -n ipu6-drivers-%{commit0} -a 1

patch -p0 -i %{SOURCE2}
cp -av ivsc-driver-%{commit1}/{backport-include,drivers,include} .
rm -fr intel-vsc-%{commit1}

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr backport-include drivers include Makefile _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        %make_build -C "${kernel_version##*___}" M=$(pwd) VERSION="v%{version}" modules
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    find _kmod_build_${kernel_version%%___*} -name "*.ko"
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 \
        _kmod_build_${kernel_version%%___*}/*.ko \
        _kmod_build_${kernel_version%%___*}/drivers/media/i2c/*.ko \
        _kmod_build_${kernel_version%%___*}/drivers/media/pci/intel/ipu6/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Tue Aug 06 2024 Simone Caronni <negativo17@gmail.com> - 0-8.20240514git9369b88
- Update to latest snapshot.

* Thu Jul 04 2024 Simone Caronni <negativo17@gmail.com> - 0-7.20240624gitaecec2a
- Update to latest snapshot.
- Don't generate tarball outside of SPEC file.

* Sat Jun 22 2024 Simone Caronni <negativo17@gmail.com> - 0-6.20240618gitbef7b04
- Fix VSC installation.

* Fri Jun 21 2024 Simone Caronni <negativo17@gmail.com> - 0-5.20240618gitbef7b04
- Update to latest snapshot.

* Fri Jun 21 2024 Simone Caronni <negativo17@gmail.com> - 0-4.20240605git404740a
- Update to latest snapshot.
- Use jwrdegoeds's fork for contributions and include ivsc driver.

* Wed Jun 05 2024 Simone Caronni <negativo17@gmail.com> - 0-3.20240605git404740a
- Update to latest snapshot.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 0-2.20240509git6fcc4c5
- Patch 0 merged upstream.

* Mon May 06 2024 Simone Caronni <negativo17@gmail.com> - 0-1.20240418git71e0c69
- First build.
