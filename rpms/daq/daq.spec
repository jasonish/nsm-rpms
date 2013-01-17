%define realname daq

Summary: Sourcefire Data Acquisition Library
Name: nsm-daq
Version: 2.0.0
Release: 2%{?dist}
License: GPL
Group: NSM
URL: http://www.snort.org/
Source0: %{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Obsoletes: nsm-libdaq

BuildRequires: libpcap-devel, libdnet-devel, libnetfilter_queue-devel
BuildRequires: flex, bison

Requires: libpcap, libdnet, libnetfilter_queue

%description
Sourcefire data acquisition library.


%prep
%setup -q -n %{realname}-%{version}


%build
./configure --prefix=%{nsm_prefix} --enable-static --disable-shared
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{nsm_prefix}/bin/daq-modules-config
%{nsm_prefix}/include/*
%{nsm_prefix}/lib/*
%doc README COPYING ChangeLog 


%changelog
* Tue Dec  4 2012 Jason Ish <ish@unx.ca> - 2.0.0-1
- Update to 2.0.0.

* Mon Jul 30 2012 Jason Ish <ish@unx.ca> - 1.1.1-1
- Update to 1.1.1

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 0.6.2-1
- Make public

