%define _defaultdocdir %{nsm_prefix}/share/doc

%define realname snort
%define nsm_prefix /opt/nsm

Summary: SNORT(R): An open source Network Intrusion Detection System (NIDS)
Name: nsm-snort2.9.4
Version: 2.9.4
Release: 2%{?dist}
License: GPL
Group: NSM
URL: http://www.snort.org/
Source0: %{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: libpcap-devel, pcre-devel, libdnet-devel, zlib-devel
BuildRequires: flex, bison
BuildRequires: libnetfilter_queue-devel
BuildRequires: nsm-libdaq >= 2.0.0-1

Requires: libpcap, pcre, libdnet, libnetfilter_queue, zlib
Requires: nsm-snort-select >= 0.3

%define app_prefix %{nsm_prefix}/packages/%{realname}/%{version}

%description
SNORT(R): An open source Network Intrusion Detection System (NIDS).


%prep
%setup -q -n %{realname}-%{version}


%build
PATH=%{nsm_prefix}/bin:$PATH \
	./configure \
	--prefix=%{app_prefix} \
	--enable-static-daq \
	--with-daq-libraries=%{nsm_prefix}/lib \
	--with-daq-includes=%{nsm_prefix}/include \
	--enable-ipv6 --enable-gre --enable-mpls --enable-targetbased --enable-decoder-preprocessor-rules --enable-ppm --enable-perfprofiling --enable-zlib --enable-active-response --enable-normalizer --enable-reload --enable-react --enable-flexresp3
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove devel type stuff that is not required for running Snort.
rm -rf $RPM_BUILD_ROOT/%{app_prefix}/src
rm -rf $RPM_BUILD_ROOT/%{app_prefix}/include

# Remove docs installed by make install. They will be included in the
# %files section below.
rm -rf $RPM_BUILD_ROOT/%{app_prefix}/share/doc


%clean
rm -rf $RPM_BUILD_ROOT


%posttrans
%{nsm_prefix}/bin/snort-select --if-not-set %{version}


%postun
if [ "$1" == "0" ]; then
   # Cleanup.
   rm -rf %{app_prefix}
fi


%files
%defattr(-,root,root,-)
%{app_prefix}/*
%doc ChangeLog COPYING LICENSE RELEASE.NOTES doc/*


%changelog
* Wed Jan  2 2013 Jason Ish <ish@unx.ca> - 2.9.4-2
- Install to a version specific prefix.

* Tue Dec  4 2012 Jason Ish <ish@unx.ca> - 2.9.4-1
- Update for Snort 2.9.4.

* Thu Aug  9 2012 Jason Ish <ish@unx.ca> - 2.9.3.1-1
- Update for Snort 2.9.3.1

* Mon Jul 30 2012 Jason Ish <ish@unx.ca> - 2.9.3-1
- Update for Snort 2.9.3

* Fri May 18 2012 Jason Ish <ish@unx.ca> - 2.9.2.3-1
- Update for Snort 2.9.2.3

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 2.9.2.2-1
- Make public
