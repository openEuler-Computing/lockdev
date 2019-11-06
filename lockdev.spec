%global _lockdir /run/lock/lockdev
%global co_date  2011-10-07

Name: 		lockdev
Version: 	1.0.4
Release: 	0.31
Summary: 	A library for locking devices
License: 	LGPLv2
URL: 		https://alioth.debian.org/projects/lockdev/

Source0: 	lockdev-%{version}.20111007git.tar.gz

Patch0: 	0000-lockdev-euidaccess.patch
Patch1: 	0001-major-and-minor-functions-moved-to-sysmacros.h.patch

Requires: 	shadow-utils glibc systemd

BuildRequires: 	autoconf automake libtool perl-interpreter systemd perl(ExtUtils::MakeMaker)

%description
Lockdev provides a reliable way to put an exclusive lock to devices
using both FSSTND and SVr4 methods.

%package 	devel
Summary: 	The header files for the lockdev library
Requires: 	lockdev = %{version}-%{release}

%description devel
The devel for %{name}


%package        help
Summary:        The doc files for the lockdev
Requires:       lockdev = %{version}-%{release}

%description help
The doc files for %{name}

%prep
%autosetup -n lockdev-scm-%{co_date} -p1

%build
./scripts/git-version > VERSION
touch ChangeLog
autoreconf -vfi

CFLAGS="%{optflags} -D_PATH_LOCK=\\\"%{_lockdir}\\\"" \
%configure --enable-helper --disable-silent-rules

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_lockdir}
mkdir -p ${RPM_BUILD_ROOT}%{_tmpfilesdir}
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/lockdev.conf <<EOF

d %{_lockdir} 0775 root lock -
EOF

%pre
getent group lock >/dev/null 2>&1 || groupadd -g 54 -r -f lock >/dev/null 2>&1 || :

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
%tmpfiles_create %{_tmpfilesdir}/lockdev.conf
fi

%postun -p /sbin/ldconfig


%files
%{license} COPYING
%doc AUTHORS
%ghost %dir %attr(0775,root,lock) %{_lockdir}
%attr(2711,root,lock)  %{_sbindir}/lockdev
%{_tmpfilesdir}/lockdev.conf
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/lockdev.pc
%{_includedir}/*

%files help
%{_mandir}/man3/*
%{_mandir}/man8/*

%changelog
* Tue Oct 29 2019 mengxian <mengxian@huawei.com> - 1.0.4-0.31
- Type:NA
- ID:NA
- SUG:NA
- DESC:Fix last changelog problem which include a macro

* Tue Oct 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.4-0.30
- Fix compile problem: add parameter for macro tmpfiles_create

* Mon Aug 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.4-0.29
- Package init
