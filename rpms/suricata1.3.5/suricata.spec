%define _defaultdocdir %{nsm_prefix}/share/doc

%define realname suricata
%define nsm_prefix /opt/nsm

Summary: The Suricata Open Source Intrusion Detection and Prevention Engine
Name: nsm-suricata1.3.5
Version: 1.3.5
Release: 2%{?dist}
License: GPL
Group: NSM
URL: http://www.openinfosecfoundation.org/
Source0: http://www.openinfosecfoundation.org/download/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: pcre-devel, libyaml-devel, libpcap-devel, file-devel, zlib-devel
BuildRequires: libnetfilter_queue-devel

Requires: pcre, libyaml, libpcap, file, zlib, libnetfilter_queue
Requires: nsm-suricata-select >= 0.3

%define app_prefix  %{nsm_prefix}/packages/%{realname}/%{version}
%define app_datadir %{app_prefix}/share


%description 
The Suricata Engine is an Open Source Next Generation Intrusion
Detection and Prevention Engine


%prep
%setup -q -n %{realname}-%{version}


%build

build_libhtp() {
    pushd libhtp
    ./configure --prefix=%{nsm_prefix} \
    		--enable-shared=no --enable-static=yes
    make
    popd
}

build_suricata() {
    build_libhtp
    ./configure \
	--prefix=%{app_prefix} \
	--enable-af-packet \
	--enable-nfqueue \
	$@
    make
}

build_suricata --enable-profiling --enable-debug
cp src/suricata src/suricata-debug
make distclean
build_suricata


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -m 0755 src/suricata-debug \
	$RPM_BUILD_ROOT%{app_prefix}/bin/suricata-debug

install -d -m 0755 $RPM_BUILD_ROOT%{app_datadir}
install -m 0644 suricata.yaml $RPM_BUILD_ROOT%{app_datadir}/
install -m 0644 classification.config $RPM_BUILD_ROOT%{app_datadir}/
install -m 0644 reference.config $RPM_BUILD_ROOT%{app_datadir}/

# Install the rules that are included with the distribution, even though
# they are not needed if you get your rules from ET.
install -d -m 0755 $RPM_BUILD_ROOT%{app_datadir}/rules
for file in rules/*.rules; do
  install -m 0644 $file $RPM_BUILD_ROOT%{app_datadir}/rules
done

# Remove the doc directory as installed by Suricata, RPM will take
# care of these files for us.
rm -rf $RPM_BUILD_ROOT%{app_prefix}/share/doc/suricata

# Remove stuff we don't want to include in the RPM.
rm -rf $RPM_BUILD_ROOT/%{app_prefix}/include
rm -rf $RPM_BUILD_ROOT/%{app_prefix}/lib
rm -rf $RPM_BUILD_ROOT/%{app_prefix}/share/doc


%clean
rm -rf $RPM_BUILD_ROOT


%posttrans
%{nsm_prefix}/bin/suricata-select --if-not-set %{version}


%postun
if [ "$1" == "0" ]; then
   # Cleanup.
   rm -rf %{app_prefix}
fi


%files
%defattr(-,root,root,-)
%{app_prefix}/*
%doc COPYING LICENSE ChangeLog


%changelog
* Wed Jan  2 2013 Jason Ish <ish@unx.ca> - 1.3.5-2
- Install to a version specific prefix.

* Thu Dec  6 2012 Jason Ish <ish@unx.ca> - 1.3.5-1
- Update to 1.3.5.

* Fri Nov 16 2012 Jason Ish <ish@unx.ca> - 1.3.4-1
- Update to 1.3.4.

* Thu Oct  4 2012 Jason Ish <ish@unx.ca> - 1.3.2-1
- Update for Suricata 1.3.2.

* Thu Sep  6 2012 Jason Ish <ish@unx.ca> - 1.3.1-2
- Use the generated suricata.yaml

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.2.1-1
- Make public
