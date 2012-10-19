%define realname barnyard2

%define _prefix /opt/nsm
%define _sysconfdir %{_prefix}/etc

Summary: Barnyard2: A reader for SNORT(R) unified2 log files
Name: nsm-barnyard2
Version: 1.10
Release: 1%{?dist}
License: GPL
Group: NSM
URL: http://www.securixlive.com/barnyard2/index.php
Source0: barnyard2-1.10.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: libtool
BuildRequires: libpcap-devel, mysql-devel, postgresql-devel

Requires: libpcap, mysql-libs
Requires: postgresql-libs

%define nsm_datadir %{_datadir}/%{realname}-%{version}

%description

Barnyard2 is a fork of the original barnyard project, designed
specifically for Snort's new unified2 file format. Barnyard2 is under
active development and continues to adapt based on user feedback.  

The current release of 2-1.8 has the following features:

- Offloads output processing of your Snort alert files to a dedicated
  process, minimising dropped packets in Snort itself.

- Parses unified2 files.

- Uses similar configuration syntax to that of Snort to simplify deployment.

- Supports all Snort output plugins (except alert_sf_socket) as well
  as two additional plugins (Sguil and CEF).

Barnyard2 has been written from the ground up and leveraging off of
Snort's core routines and is continually aligned to the latest
releases of Snort. It is released under the GPLv2 licence.


%prep
%setup -q -n firnsy-barnyard2-2f5d496


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
