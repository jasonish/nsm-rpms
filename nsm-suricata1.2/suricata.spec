%define _prefix /opt/nsm
%define realname suricata
%define major_version 1.2

Summary: The Suricata Open Source Intrusion Detection and Prevention Engine
Name: nsm-suricata1.2
Version: 1.2.1
Release: 1%{?dist}
License: GPL
Group: NSM
URL: http://www.openinfosecfoundation.org/
Source0: http://www.openinfosecfoundation.org/download/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: pcre-devel, libyaml-devel, libpcap-devel, file-devel, zlib-devel
BuildRequires: libnetfilter_queue-devel

Requires: pcre, libyaml, libpcap, file, zlib, libnetfilter_queue
Requires: nsm-suricata-select >= 0.01

%description 
The Suricata Engine is an Open Source Next Generation Intrusion
Detection and Prevention Engine

%define configure_args --enable-af-packet --enable-nfqueue

%prep
%setup -q -n %{realname}-%{version}


%build

# Build libhtp and cache.  I should probably have a libhtp package!
pushd libhtp
%configure --enable-shared=no --enable-static=yes
make
popd
cp -a libhtp libhtp.cached

# Build Suricata with debug and profiling.
%configure %{configure_args} --enable-profiling --enable-debug
make
cp src/suricata src/suricata-debug

make distclean
mv libhtp libhtp.orig
mv libhtp.cached libhtp

%configure %{configure_args}
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_bindir}/suricata \
	$RPM_BUILD_ROOT%{_bindir}/suricata%{major_version}
install -m 0755 src/suricata-debug \
	$RPM_BUILD_ROOT%{_bindir}/suricata-debug%{major_version}

# Cleanup.
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_bindir}/suricata-select --if-not-set %{major_version}

%files
%defattr(-,root,root,-)
%{_bindir}/suricata%{major_version}
%{_bindir}/suricata-debug%{major_version}
%doc COPYING LICENSE ChangeLog doc/*

# Not really doc, should probably go in a better place.
%doc suricata.yaml classification.config reference.config

%changelog
* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.2.1-1
- Make public

