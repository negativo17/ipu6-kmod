%global date 20250215
%global commit0 40f52831a1bd234961b989d921113bb7603233b2
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 0eae85556558b410635ad03ed5eccb9648e11fce
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:       ipu6-kmod
Version:    0.0^%{date}git%{shortcommit0}
Release:    2%{?dist}
Summary:    Kernel drivers for the IPU 6 and sensors
License:    GPL-3.0-only
URL:        https://github.com/jwrdegoede/ipu6-drivers

Source0:    %{url}/archive/%{commit0}.tar.gz#/ipu6-drivers-%{shortcommit0}.tar.gz
Source1:    https://github.com/jwrdegoede/usbio-drivers/archive/%{commit1}.tar.gz#/usbio-drivers-%{shortcommit1}.tar.gz

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
cp -fr usbio-drivers*/{drivers,include} .
patch -p1 -i patches/*.patch

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr drivers include Makefile _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        %make_build -C "${kernel_version##*___}" M=$(pwd) VERSION="v%{version}" modules
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    # Print out modules that are getting built:
    find _kmod_build_${kernel_version%%___*} -name "*.ko"
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 \
        _kmod_build_${kernel_version%%___*}/*.ko \
        _kmod_build_${kernel_version%%___*}/drivers/media/i2c/*.ko \
        _kmod_build_${kernel_version%%___*}/drivers/media/pci/intel/ipu6/psys/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Sat Feb 15 2025 Simone Caronni <negativo17@gmail.com> - 0.0^20250215git40f5283-2
- Update to latest snapshot.

* Tue Jan 21 2025 Simone Caronni <negativo17@gmail.com> - 0.0^20250119gitf2a1b54-1
- Update to latest jwrdegoede snapshot.
- Switch to recent packaging guidelines for snapshots.

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
