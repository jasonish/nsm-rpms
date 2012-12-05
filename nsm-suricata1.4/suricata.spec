%define _prefix /opt/nsm
%define realname suricata

%define version_suffix rc1

Summary: The Suricata Open Source Intrusion Detection and Prevention Engine
Name: nsm-suricata1.4
Version: 1.4
Release: 0.1.rc1%{?dist}
License: GPL
Group: NSM
URL: http://www.openinfosecfoundation.org/
Source0: http://www.openinfosecfoundation.org/download/%{realname}-%{version}%{?version_suffix}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}%{?version_suffix}-%{release}-root

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
%setup -q -n %{realname}-%{version}%{?version_suffix}


%build

build_libhtp() {
    if [ -e libhtp.cache ]; then
        rm -rf libhtp
        cp -a libhtp.cache libhtp
    else
        pushd libhtp
        %configure --enable-shared=no --enable-static=yes
        make
        popd
	cp -a libhtp libhtp.cache
    fi
}

build_suricata() {
    build_libhtp
    %configure %{configure_args} $@
    make
}

build_suricata --enable-profiling --enable-debug
cp src/suricata src/suricata-debug
make distclean
build_suricata


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_bindir}/suricata \
	$RPM_BUILD_ROOT%{_bindir}/suricata%{version}
mv $RPM_BUILD_ROOT%{_bindir}/suricatasc \
 	$RPM_BUILD_ROOT%{_bindir}/suricatasc%{version}
install -m 0755 src/suricata-debug \
	$RPM_BUILD_ROOT%{_bindir}/suricata-debug%{version}

install -d -m 0755 $RPM_BUILD_ROOT%{appdatadir}
install -m 0644 suricata.yaml $RPM_BUILD_ROOT%{appdatadir}/
install -m 0644 classification.config $RPM_BUILD_ROOT%{appdatadir}/
install -m 0644 reference.config $RPM_BUILD_ROOT%{appdatadir}/
install -m 0644 threshold.config $RPM_BUILD_ROOT%{appdatadir}/

# Install the rules that are included with the distribution, even though
# they are not needed if you get your rules from ET.
install -d -m 0755 $RPM_BUILD_ROOT%{appdatadir}/rules
for file in rules/*.rules; do
  install -m 0644 $file $RPM_BUILD_ROOT%{appdatadir}/rules
done

# Remove the doc directory as installed by Suricata, RPM will take
# care of these files for us.
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/doc/suricata

# Cleanup.
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_bindir}/suricata-select --if-not-set %{version}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%doc COPYING LICENSE ChangeLog doc/*
%{appdatadir}/*


%changelog
* Thu Nov 29 2012 Jason Ish <ish@unx.ca> - 1.4-0.1.rc1
- Update to 1.4rc1.

* Fri Nov 16 2012 Jason Ish <ish@unx.ca> - 1.3.4-1
- Update to 1.3.4.

* Thu Oct  4 2012 Jason Ish <ish@unx.ca> - 1.3.2-1
- Update for Suricata 1.3.2.

* Thu Sep  6 2012 Jason Ish <ish@unx.ca> - 1.3.1-2
- Use the generated suricata.yaml

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.2.1-1
- Make public
