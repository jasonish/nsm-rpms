%define realname daq
%define _prefix /opt/nsm

Summary: Sourcefire Data Acquisition Library
Name: nsm-libdaq
Version: 1.1.1
Release: 1%{?dist}
License: GPL
Group: NSM
URL: http://www.snort.org/
Source0: http://sourceforge.net/projects/snort/files/snort/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: libpcap-devel, libdnet-devel, libnetfilter_queue-devel
BuildRequires: flex, bison

Requires: libpcap, libdnet, libnetfilter_queue

%description
Sourcefire data acquisition library.


%prep
%setup -q -n %{realname}-%{version}


%build
%configure
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# We only want to depend on DAQ for building, not for runing.  So kill off
# the shared libraries.
rm -rf $RPM_BUILD_ROOT%{_libdir}/daq
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so.*
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.a
%doc README COPYING ChangeLog 


%changelog
* Mon Jul 30 2012 Jason Ish <ish@unx.ca> - 1.1.1-1
- Update to 1.1.1

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 0.6.2-1
- Make public

