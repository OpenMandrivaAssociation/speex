%define	name	speex
%define	major	1
%define	libname	 %mklibname %name %major
%define version 1.2
%define beta beta1
%define release %mkrel 0.%beta.1

Summary:	An open-source, patent-free speech codec
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Sound
Source0:	http://downloads.us.xiph.org/releases/speex/%{name}-%{version}%beta.tar.bz2
Patch1:		speex-1.1.6-fix-pkgconfig-path.patch
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

%package -n	%{libname}-devel
Summary:	Speex development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
Speex development files.

%package -n	%{libname}-static-devel
Summary:	Speex static library 
Group:		Development/C
Requires:	%{libname}-devel = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
Speex static library for developing applications based on Speex.

%prep
%setup -q -n %name-%version%beta
%patch1 -p1 -b .pkgconfig
autoconf

%build
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

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING AUTHORS ChangeLog NEWS README
%{_mandir}/man1/speexenc.1*
%{_mandir}/man1/speexdec.1*
%attr(755,root,root) %{_bindir}/speex*

%files -n %{libname}
%attr(755,root,root) %{_libdir}/libspeex.so.%{major}*

%files -n %{libname}-devel
%defattr(644,root,root,755)
%doc doc/manual.pdf
%{_libdir}/libspeex*.la
%{_libdir}/libspeex*.so
%{_includedir}/speex
%{_libdir}/pkgconfig/speex.pc
%{_datadir}/aclocal/speex.m4

%files -n %{libname}-static-devel
%defattr(644,root,root,755)
%{_libdir}/libspeex*.a


