%define	name	speex
%define version 1.2
%define beta rc1
%define release %mkrel 0.%beta.1
%define	major	1
%define	libname	 %mklibname %name %major
%define develname %mklibname -d %name
%define staticname %mklibname -s -d %name

Summary:	An open-source, patent-free speech codec
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Sound
Source0:	http://downloads.us.xiph.org/releases/speex/%{name}-%{version}%beta.tar.gz
Patch1:		speex-1.1.6-fix-pkgconfig-path.patch
Patch2:		speex-1.2rc1-CVE-2008-1686.patch
URL:		http://www.speex.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	oggvorbis-devel
BuildRequires:	chrpath
#gw if patched
BuildRequires:	autoconf2.5

%description
Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%package -n	%{libname}
Summary:	Shared library of the Speex codec
Group:		System/Libraries

%description -n	%{libname}
Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

This package contains the shared library required for running
applications based on Speex.

%package -n	%develname
Summary:	Speex development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes: %mklibname -d %name 1

%description -n	%develname
Speex development files.

%package -n	%staticname
Summary:	Speex static library 
Group:		Development/C
Requires:	%develname = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Obsoletes: %mklibname -s -d %name 1

%description -n %staticname
Speex static library for developing applications based on Speex.

%prep
%setup -q -n %name-%version%beta
%patch1 -p1 -b .pkgconfig
%patch2 -p1 -b .cve-2008-1686

%build
autoreconf -fi
export CFLAGS='%optflags -DRELEASE'
%if %mdkversion <= 1000
%define __libtoolize true
%endif
%configure2_5x --with-ogg-libraries=%{_libdir}
make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}
chrpath -d %buildroot%_bindir/*
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/*/manual.pdf

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc COPYING AUTHORS ChangeLog NEWS README
%{_mandir}/man1/speexenc.1*
%{_mandir}/man1/speexdec.1*
%attr(755,root,root) %{_bindir}/speex*

%files -n %{libname}
%defattr(755,root,root)
%{_libdir}/libspeex.so.%{major}*
%{_libdir}/libspeexdsp.so.%{major}*

%files -n %develname
%defattr(644,root,root,755)
%doc doc/manual.pdf
%{_libdir}/libspeex*.la
%{_libdir}/libspeex*.so
%{_includedir}/speex
%{_libdir}/pkgconfig/speex.pc
%{_libdir}/pkgconfig/speexdsp.pc
%{_datadir}/aclocal/speex.m4

%files -n %staticname
%defattr(644,root,root,755)
%{_libdir}/libspeex*.a


