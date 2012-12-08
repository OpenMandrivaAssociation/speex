%define beta rc1

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	An open-source, patent-free speech codec
Name:		speex
Version:	1.2
Release:	0.%{beta}.7
License:	BSD
Group:		Sound
URL:		http://www.speex.org/
Source0:	http://downloads.us.xiph.org/releases/speex/%{name}-%{version}%{beta}.tar.gz
Patch1:		speex-1.1.6-fix-pkgconfig-path.patch
Patch2:		speex-1.2rc1-CVE-2008-1686.patch

BuildRequires:	pkgconfig(vorbis)
BuildRequires:	chrpath

%description
Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%package -n	%{libname}
Summary:	Shared library of the Speex codec
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library required for running
applications based on Speex.

%package -n	%{develname}
Summary:	Speex development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -s -d speex} < 1.2-0.rc1.7

%description -n	%{develname}
Speex development files.

%prep
%setup -qn %{name}-%{version}%{beta}
%apply_patches

%build
autoreconf -fi
export CFLAGS='%{optflags} -DRELEASE'
%configure2_5x \
	--disable-static \
	--with-ogg-libraries=%{_libdir}
make

%install
%makeinstall_std
chrpath -d %{buildroot}%{_bindir}/*
rm -f %{buildroot}%{_datadir}/doc/*/manual.pdf

%files
%doc COPYING AUTHORS ChangeLog NEWS README
%{_mandir}/man1/speexenc.1*
%{_mandir}/man1/speexdec.1*
%attr(755,root,root) %{_bindir}/speex*

%files -n %{libname}
%{_libdir}/libspeex.so.%{major}*
%{_libdir}/libspeexdsp.so.%{major}*

%files -n %{develname}
%doc doc/manual.pdf
%{_libdir}/libspeex*.so
%{_includedir}/speex
%{_libdir}/pkgconfig/speex.pc
%{_libdir}/pkgconfig/speexdsp.pc
%{_datadir}/aclocal/speex.m4


%changelog
* Fri Apr 27 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.2-0.rc1.6
+ Revision: 793724
- rebuild
- cleaned up spec

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-0.rc1.5
+ Revision: 670008
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-0.rc1.4mdv2011.0
+ Revision: 607555
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-0.rc1.3mdv2010.1
+ Revision: 521163
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.2-0.rc1.2mdv2010.0
+ Revision: 427207
- rebuild

* Tue Apr 07 2009 Funda Wang <fwang@mandriva.org> 1.2-0.rc1.1mdv2009.1
+ Revision: 364635
- rediff patch2

* Thu Jul 24 2008 Funda Wang <fwang@mandriva.org> 1.2-0.rc1.1mdv2009.0
+ Revision: 245332
- New version 1.2 rc1

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Apr 30 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.2-0.beta3.2mdv2009.0
+ Revision: 199383
- P2: security fix for CVE-2008-1686

* Tue Feb 05 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1.2-0.beta3.1mdv2008.1
+ Revision: 162560
- new version
- update file list
- new devel name

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu May 24 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.2-0.beta2.1mdv2008.0
+ Revision: 30801
- new version


* Fri Jan 05 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.2-0.beta1.1mdv2007.0
+ Revision: 104489
- Import speex

* Fri Jan 05 2007 Götz Waschk <waschk@mandriva.org> 1.2-0.beta1.1mdv2007.1
- new version

* Fri Aug 25 2006 Götz Waschk <waschk@mandriva.org> 1.1.12-3mdv2007.0
- remove rpath

* Mon Aug 21 2006 Pascal Terjan <pterjan@mandriva.org> 1.1.12-2mdv2007.0
- Have speex build even if i586 version of libogg is installed
- Fix macro in changelog

* Thu Mar 02 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.1.12-1mdk
- New release 1.1.12
- use mkrel

* Tue Dec 06 2005 GÃ¶tz Waschk <waschk@mandriva.org> 1.1.11.1-1mdk
- New release 1.1.11.1

* Thu Nov 24 2005 Götz Waschk <waschk@mandriva.org> 1.1.11-1mdk
- disable parallel build
- New release 1.1.11

* Tue Aug 09 2005 Götz Waschk <waschk@mandriva.org> 1.1.10-2mdk
- remove mdkversion macro

* Sat Jun 25 2005 Götz Waschk <waschk@mandriva.org> 1.1.10-1mdk
- new source URL
- New release 1.1.10

* Mon Jun 13 2005 Götz Waschk <waschk@mandriva.org> 1.1.9-1mdk
- New release 1.1.9

* Fri May 20 2005 Götz Waschk <waschk@mandriva.org> 1.1.8-1mdk
- New release 1.1.8

* Thu Mar 03 2005 GÃ¶tz Waschk <waschk@linux-mandrake.com> 1.1.7-1mdk
- New release 1.1.7

* Wed Jan 19 2005 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 1.1.6-2mdk
- fix path to headers for pkgconfig (P1)
- add provides
- cosmetics

* Sat Jul 31 2004 Götz Waschk <waschk@linux-mandrake.com> 1.1.6-1mdk
- update file list
- reenable libtoolize
- rediff patch 0
- New release 1.1.6

* Fri Apr 23 2004 GÃ¶tz Waschk <waschk@linux-mandrake.com> 1.1.5-1mdk
- make it rpmbuildupdate compatible
- New release 1.1.5

* Thu Jan 22 2004 GÃ¶tz Waschk <waschk@linux-mandrake.com> 1.1.4-1mdk
- don't run libtoolize
- fix buildrequires
- use the autoconf2.5 macro
- new version

