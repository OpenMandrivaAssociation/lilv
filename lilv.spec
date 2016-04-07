%define _enable_debug_packages %{nil}
%define debug_package          %{nil}
%define lib_major       0
%define lib_name        %mklibname %{name} %{lib_major}
%define lib_name_devel  %mklibname %{name} -d

Name:           lilv
Version:        0.22.0
Release:        1
Summary:        LV2 plugin library for applications and hosts
Source0:        http://download.drobilla.net/%{name}-%{version}.tar.bz2
Patch0:         lilv-0.5.0-fix-decl.patch
URL:            http://drobilla.net/software/%{name}/
License:        ISC
Group:          System/Libraries

BuildRequires:  waf, pkgconfig, python
BuildRequires:  sord-devel
BuildRequires:  pkgconfig(lv2)
BuildRequires:  sratom-devel

%description
LV2 plugin library for applications and hosts

%files -n %{name}
%doc COPYING README
%doc %{_mandir}/man1/lv2info.1.xz
%doc %{_mandir}/man1/lv2ls.1.xz
%{_bindir}/lilv-bench
%{_bindir}/lv2info
%{_bindir}/lv2ls
%{_bindir}/lv2bench
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/bash_completion.d/lilv

#-----------------------------------
%package -n %{lib_name}

Summary:        LV2 plugin library for applications and hosts
Group:          System/Libraries

%description -n %{lib_name}
Lilv is a library to make the use of LV2 plugins as simple as possible
for applications. Lilv is the successor to SLV2, rewritten to be
significantly faster and have minimal dependencies.

%files -n %{lib_name}
%{_libdir}/lib%{name}-%{lib_major}.so.*

#-----------------------------------
%package -n %{lib_name_devel}
Summary:        Headers for the lilv LV2 library
Group:          System/Libraries
Requires:       %{lib_name} = %{version}-%{release}
Requires:       pkgconfig
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{lib_name_devel}
Development files needed to build applications against lilv.

%files -n %{lib_name_devel}
%{_libdir}/lib%{name}-%{lib_major}.so
%dir %{_includedir}/%{name}-%{lib_major}/%{name}
%{_includedir}/%{name}-%{lib_major}/%{name}/*.h
%{_includedir}/%{name}-%{lib_major}/%{name}/*.hpp
%{_libdir}/pkgconfig/%{name}-%{lib_major}.pc

#-----------------------------------
%prep
%setup -q
sed -i -e 's/^.*run_ldconfig/#\0/' wscript

%build
%{__python2} ./waf configure --prefix=%{_prefix} \
		CC=%{__cc} \
                --mandir=%{_mandir} \
                --libdir=%{_libdir} \
                --configdir=%{_sysconfdir}
%{__python2} ./waf

%install

%{__python2} ./waf install --destdir=%{buildroot}
