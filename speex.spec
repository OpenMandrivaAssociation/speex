# Speex is used by pulseaudio, pulseaudio is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define lib32name %mklib32name %{name} %{major}
%define devel32name %mklib32name -d %{name}
%global optflags %{optflags} -O3

Summary:	An open-source, patent-free speech codec
Name:		speex
Version:	1.2.1
Release:	2
License:	BSD
Group:		Sound
URL:		http://www.speex.org/
Source0:	http://downloads.us.xiph.org/releases/speex/%{name}-%{version}.tar.gz
Patch1:		speex-1.1.6-fix-pkgconfig-path.patch
Patch2:		speex-1.2rc1-CVE-2008-1686.patch

BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
%if %{with compat32}
BuildRequires:	devel(libogg)
BuildRequires:	devel(libvorbis)
%endif
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

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared library of the Speex codec (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the shared library required for running
applications based on Speex.

%package -n %{devel32name}
Summary:	Speex development files (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{version}
Requires:	%{develname} = %{version}

%description -n	%{devel32name}
Speex development files.
%endif

%prep
%autosetup -p1
autoreconf -fi
export CFLAGS='%{optflags} -DRELEASE'
export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--disable-binaries \
	--with-ogg-libraries=%{_prefix}/lib
cd ..
%endif

mkdir build
cd build
%configure \
	--disable-static \
	--enable-binaries \
	--with-ogg-libraries=%{_libdir}

# Remove rpath from speexenc and speexdec
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build
chrpath -d %{buildroot}%{_bindir}/*
rm -f %{buildroot}%{_datadir}/doc/*/manual.pdf

%files
%doc COPYING AUTHORS ChangeLog NEWS README
%doc %{_mandir}/man1/speexenc.1*
%doc %{_mandir}/man1/speexdec.1*
%attr(755,root,root) %{_bindir}/speex*

%files -n %{libname}
%{_libdir}/libspeex.so.%{major}*

%files -n %{develname}
%doc doc/manual.pdf
%{_libdir}/libspeex*.so
%{_includedir}/speex
%{_libdir}/pkgconfig/speex.pc
%{_datadir}/aclocal/speex.m4

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libspeex.so.%{major}*

%files -n %{devel32name}
%{_prefix}/lib/libspeex*.so
%{_prefix}/lib/pkgconfig/speex.pc
%endif
