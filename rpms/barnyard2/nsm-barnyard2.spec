%define realname barnyard2

%define _prefix /opt/nsm
%define _sysconfdir %{_prefix}/etc

Summary: Barnyard2: A reader for SNORT(R) unified2 log files
Name: nsm-barnyard2
Version: 1.11
Release: 1%{?dist}
License: GPL
Group: NSM
URL: http://www.securixlive.com/barnyard2/index.php
Source0: barnyard2-1.11.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: libtool
BuildRequires: libpcap-devel, mysql-devel, postgresql-devel

Requires: libpcap, mysql-libs
Requires: postgresql-libs

%define nsm_datadir %{_datadir}/%{realname}-%{version}

%description
Barnyard2 is a dedicated spooler for Snort's unified2 binary output format.


%prep
#%setup -q -n firnsy-barnyard2-4dfdc80
%setup -q -n barnyard2-ish-v2-1.11


%build
./autogen.sh
%configure \
	--with-mysql \
%ifarch x86_64
	--with-mysql-libraries=/usr/lib64/mysql \
%else
	--with-mysql-libraries=/usr/lib/mysql \
%endif
	--with-postgresql
make


%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 755 src/barnyard2 $RPM_BUILD_ROOT%{_bindir}/

%{__mkdir_p} $RPM_BUILD_ROOT%{nsm_datadir}
%{__install} -m 644 etc/barnyard2.conf $RPM_BUILD_ROOT%{nsm_datadir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{nsm_datadir}/*
%doc LICENSE RELEASE.NOTES README COPYING
%doc doc/INSTALL doc/README.*


%changelog
* Fri Oct 19 2012 Jason Ish <ish@unx.ca> - 1.10-1
- Update to v1.10 release.

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.10-0.1.beta2
- Make public.
