%define realname daemonlogger
%define _prefix /opt/nsm

Summary: Daemonlogger(TM) is a packet logger and soft tap
Name: nsm-daemonlogger
Version: 1.2.1
Release: 1%{?dist}
License: GPLv2
Group: NSM
URL: http://www.snort.org
Source0: http://ftp.freebsd.org/pub/FreeBSD/ports/distfiles/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: libpcap-devel, libdnet-devel

Requires: libpcap, libdnet

%description
Daemonlogger(TM) is a packet logger and soft tap developed by Martin
Roesch. The libpcap-based program has two runtime modes:

1. It sniffs packets and spools them straight to the disk and can
daemonize itself for background packet logging. By default the file
rolls over when 2 GB of data is logged.

2. It sniffs packets and rewrites them to a second interface,
essentially acting as a soft tap. It can also do this in daemon mode.
These two runtime modes are mutually exclusive, if the program is
placed in tap mode (using the -I switch) then logging to disk is
disabled.

%prep
%setup -q -n %{realname}-%{version}


%build
%configure
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/daemonlogger
%doc AUTHORS COPYING INSTALL NEWS README


%changelog
* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.2.1-1
- Make public

