%define _prefix /opt/nsm
%define realname suricata

Summary: The Suricata Open Source Intrusion Detection and Prevention Engine
Name: nsm-suricata1.3.2
Version: 1.3.2
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

%define appdatadir %{_datadir}/suricata%{version}

%define configure_args --enable-af-packet --enable-nfqueue


%description 
The Suricata Engine is an Open Source Next Generation Intrusion
Detection and Prevention Engine


%prep
%setup -q -n %{realname}-%{version}


%build

build_libhtp() {
    pushd libhtp
    %configure --enable-shared=no --enable-static=yes
    make
    popd
}

# Build Suricata with debug and profiling.
build_libhtp
%configure %{configure_args} --enable-profiling --enable-debug
make
cp src/suricata src/suricata-debug

make distclean

build_libhtp
%configure %{configure_args}
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_bindir}/suricata \
	$RPM_BUILD_ROOT%{_bindir}/suricata%{version}
install -m 0755 src/suricata-debug \
	$RPM_BUILD_ROOT%{_bindir}/suricata-debug%{version}

install -d -m 0755 $RPM_BUILD_ROOT%{appdatadir}
install -m 0644 suricata.yaml $RPM_BUILD_ROOT%{appdatadir}/suricata.yaml
install -m 0644 classification.config $RPM_BUILD_ROOT%{appdatadir}/
install -m 0644 reference.config $RPM_BUILD_ROOT%{appdatadir}/

install -d -m 0755 $RPM_BUILD_ROOT%{appdatadir}/rules
for file in rules/*.rules; do
  install -m 0644 $file $RPM_BUILD_ROOT%{appdatadir}/rules
done

# Cleanup.
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_bindir}/suricata-select --if-not-set %{version}

%files
%defattr(-,root,root,-)
%{_bindir}/suricata%{version}
%{_bindir}/suricata-debug%{version}
%doc COPYING LICENSE ChangeLog doc/*
%{appdatadir}/*

# Not really doc, should probably go in a better place.
%doc suricata.yaml classification.config reference.config

%changelog
* Thu Oct  4 2012 Jason Ish <ish@unx.ca> - 1.3.2-1
- Update for Suricata 1.3.2.

* Thu Sep  6 2012 Jason Ish <ish@unx.ca> - 1.3.1-2
- Use the generated suricata.yaml

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.2.1-1
- Make public

