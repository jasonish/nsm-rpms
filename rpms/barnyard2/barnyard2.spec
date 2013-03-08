%define realname barnyard2

Summary: Barnyard2: A reader for SNORT(R) unified2 log files
Name: nsm-barnyard2
Version: 1.12
Release: 1%{?dist}
License: GPL
Group: NSM
URL: http://www.securixlive.com/barnyard2/index.php
Source0: barnyard2-1.12.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: libtool
BuildRequires: libpcap-devel, mysql-devel, postgresql-devel

Requires: libpcap, mysql-libs
Requires: postgresql-libs

%define app_datadir %{nsm_prefix}/share/%{realname}


%description
Barnyard2 is a dedicated spooler for Snort's unified2 binary output format.


%prep
%setup -q -n firnsy-barnyard2-3c1f553
#%setup -q -n barnyard2-ish-v2-1.11


%build
./autogen.sh
./configure --prefix=%{nsm_prefix} \
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

%{__mkdir_p} $RPM_BUILD_ROOT%{nsm_prefix}/bin
%{__install} -m 755 src/barnyard2 $RPM_BUILD_ROOT%{nsm_prefix}/bin

%{__mkdir_p} $RPM_BUILD_ROOT%{app_datadir}
%{__install} -m 644 etc/barnyard2.conf $RPM_BUILD_ROOT%{app_datadir}

%{__mkdir_p} $RPM_BUILD_ROOT%{app_datadir}/schemas
%{__install} -m 644 schemas/create_{mysql,postgresql} \
	     $RPM_BUILD_ROOT%{app_datadir}/schemas
%{__install} -m 644 schemas/SCHEMA_ACCESS $RPM_BUILD_ROOT%{app_datadir}/schemas


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{nsm_prefix}/bin/barnyard2
%{app_datadir}/barnyard2.conf
%{app_datadir}/schemas/*
%doc LICENSE RELEASE.NOTES README COPYING
%doc doc/INSTALL doc/README.*


%changelog
* Fri Mar  8 2013 Jason Ish <ish@unx.ca> - 1.12-1
- Update to 2-1.12.

* Fri Jan 11 2013 Jason Ish <ish@unx.ca> - 1.11-2
- Add schema files.

* Fri Oct 19 2012 Jason Ish <ish@unx.ca> - 1.10-1
- Update to v1.10 release.

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.10-0.1.beta2
- Make public.
