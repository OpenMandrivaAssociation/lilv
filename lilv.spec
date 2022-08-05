# Work around incomplete debug packages
%global _empty_manifest_terminate_build 0

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	LV2 plugin library for applications and hosts
Name:		lilv
Version:	0.24.16
Release:	1
License:	ISC
Group:		System/Libraries
URL:		http://drobilla.net/software/%{name}/
Source0:	http://download.drobilla.net/%{name}-%{version}.tar.xz
BuildRequires:  doxygen
BuildRequires:	meson
BuildRequires:	python
BuildRequires:	sord-devel
BuildRequires:	pkgconfig(lv2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	sratom-devel
BuildRequires:  python3dist(sphinx)

%description
LV2 plugin library for applications and hosts.

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

Summary:	LV2 plugin library for applications and hosts
Group:		System/Libraries

%description -n %{libname}
Lilv is a library to make the use of LV2 plugins as simple as possible
for applications. Lilv is the successor to SLV2, rewritten to be
significantly faster and have minimal dependencies.

%files -n %{libname}
%{_libdir}/lib%{name}-%{major}.so.*

#-----------------------------------
%package -n %{develname}
Summary:	Headers for the lilv LV2 library
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files needed to build applications against lilv.

%files -n %{develname}
%{_libdir}/lib%{name}-%{major}.so
%dir %{_includedir}/%{name}-%{major}/%{name}
%{_includedir}/%{name}-%{major}/%{name}/*.h
%{_includedir}/%{name}-%{major}/%{name}/*.hpp
%{_libdir}/pkgconfig/%{name}-%{major}.pc

#-----------------------------------

%package -n python-%{name}
Summary:	Python bindings for %{name}
Requires:	%{libname} = %{version}-%{release}

%description -n python-%{name}
%{name} is a lightweight C library for Resource Description Syntax which
supports reading and writing Turtle and NTriples.

This package contains the python libraries for %{name}.

%files -n python-%{name}
%{python_sitelib}/%{name}.*

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
