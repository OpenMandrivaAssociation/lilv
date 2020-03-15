%define _enable_debug_packages %{nil}
%define debug_package          %{nil}
%define lib_major       0
%define libname        %mklibname %{name} %{lib_major}
%define libname_devel  %mklibname %{name} -d

Name:           lilv
Version:	0.24.6
Release:	1
Summary:        LV2 plugin library for applications and hosts
Source0:        http://download.drobilla.net/%{name}-%{version}.tar.bz2
Patch0:         lilv-0.5.0-fix-decl.patch
URL:            http://drobilla.net/software/%{name}/
License:        ISC
Group:          System/Libraries

BuildRequires:  waf, pkgconfig, python
BuildRequires:  sord-devel
BuildRequires:  pkgconfig(lv2)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  sratom-devel

%description
LV2 plugin library for applications and hosts

%files -n %{name}
%doc COPYING
%doc %{_mandir}/man1/lv2info.1.*
%doc %{_mandir}/man1/lv2ls.1.*
%doc %{_mandir}/man1/lv2apply.1.*
%{_bindir}/lilv-bench
%{_bindir}/lv2info
%{_bindir}/lv2ls
%{_bindir}/lv2bench
%{_bindir}/lv2apply
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/bash_completion.d/lilv

#-----------------------------------
%package -n %{libname}

Summary:        LV2 plugin library for applications and hosts
Group:          System/Libraries

%description -n %{libname}
Lilv is a library to make the use of LV2 plugins as simple as possible
for applications. Lilv is the successor to SLV2, rewritten to be
significantly faster and have minimal dependencies.

%files -n %{libname}
%{_libdir}/lib%{name}-%{lib_major}.so.*

#-----------------------------------
%package -n %{libname_devel}
Summary:        Headers for the lilv LV2 library
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}
Requires:       pkgconfig
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{libname_devel}
Development files needed to build applications against lilv.

%files -n %{libname_devel}
%{_libdir}/lib%{name}-%{lib_major}.so
%dir %{_includedir}/%{name}-%{lib_major}/%{name}
%{_includedir}/%{name}-%{lib_major}/%{name}/*.h
%{_includedir}/%{name}-%{lib_major}/%{name}/*.hpp
%{_libdir}/pkgconfig/%{name}-%{lib_major}.pc

#-----------------------------------

%package -n python-%{name}
Summary:    Python bindings for %{name}
Requires:   %{libname} = %{version}-%{release}

%description -n python-%{name}
%{name} is a lightweight C library for Resource Description Syntax which
supports reading and writing Turtle and NTriples.

This package contains the python libraries for %{name}.

%files -n python-%{name}
%{python_sitelib}/%{name}.*
%{python_sitelib}/__pycache__/*

%prep
%setup -q
sed -i -e 's/^.*run_ldconfig/#\0/' wscript

%build
python ./waf configure --prefix=%{_prefix} \
		CC=%{__cc} \
                --mandir=%{_mandir} \
                --libdir=%{_libdir} \
                --configdir=%{_sysconfdir}
python ./waf

%install
python ./waf install --destdir=%{buildroot}
