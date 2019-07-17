%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%global optflags %{optflags} -O3

Summary:	An open-source, patent-free speech codec
Name:		speex
Version:	1.2.0
Release:	4
License:	BSD
Group:		Sound
URL:		http://www.speex.org/
Source0:	http://downloads.us.xiph.org/releases/speex/%{name}-%{version}.tar.gz
Patch1:		speex-1.1.6-fix-pkgconfig-path.patch
Patch2:		speex-1.2rc1-CVE-2008-1686.patch

BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	chrpath

%description
Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%package -n %{libname}
Summary:	Shared library of the Speex codec
Group:		System/Libraries

%description -n %{libname}
This package contains the shared library required for running
applications based on Speex.

%package -n %{develname}
Summary:	Speex development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -s -d speex} < 1.2-0.rc1.7

%description -n	%{develname}
Speex development files.

%prep
%autosetup -p1

%build
autoreconf -fi
export CFLAGS='%{optflags} -DRELEASE'
%configure \
	--disable-static \
	--enable-binaries \
	--with-ogg-libraries=%{_libdir}

# Remove rpath from speexenc and speexdec
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install
chrpath -d %{buildroot}%{_bindir}/*
rm -f %{buildroot}%{_datadir}/doc/*/manual.pdf

%files
%doc COPYING AUTHORS ChangeLog NEWS README
%{_mandir}/man1/speexenc.1*
%{_mandir}/man1/speexdec.1*
%attr(755,root,root) %{_bindir}/speex*

%files -n %{libname}
%{_libdir}/libspeex.so.%{major}*

%files -n %{develname}
%doc doc/manual.pdf
%{_libdir}/libspeex*.so
%{_includedir}/speex
%{_libdir}/pkgconfig/speex.pc
%{_datadir}/aclocal/speex.m4

