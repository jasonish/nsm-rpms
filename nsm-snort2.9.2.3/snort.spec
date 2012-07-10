%define _prefix /opt/nsm
%define realname snort

Summary: SNORT(R): An open source Network Intrusion Detection System (NIDS)
Name: nsm-snort2.9.2.3
Version: 2.9.2.3
Release: 1%{?dist}
License: GPL
Group: NSM
URL: http://www.snort.org/
Source0: http://sourceforge.net/projects/snort/files/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: libpcap-devel, pcre-devel, libdnet-devel, zlib-devel
BuildRequires: flex, bison
BuildRequires: libnetfilter_queue-devel
BuildRequires: nsm-libdaq >= 0.6.2-1

Requires: libpcap, pcre, libdnet, libnetfilter_queue, zlib
Requires: nsm-snort-select >= 0.01

%description
SNORT(R): An open source Network Intrusion Detection System (NIDS).


%prep
%setup -q -n %{realname}-%{version}


%build
PATH=%{_prefix}/bin:$PATH %configure \
	--enable-static-daq \
	--with-daq-libraries=%{_prefix}/lib \
	--with-daq-includes=%{_prefix}/include \
	--enable-ipv6 --enable-gre --enable-mpls --enable-targetbased --enable-decoder-preprocessor-rules --enable-ppm --enable-perfprofiling --enable-zlib --enable-active-response --enable-normalizer --enable-reload --enable-react --enable-flexresp3
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

for f in snort u2boat u2spewfoo; do
	mv $RPM_BUILD_ROOT%{_bindir}/${f} \
		$RPM_BUILD_ROOT%{_bindir}/${f}%{version}
done

# Perhaps we need a -devel package, but for now just delete the devel
# type stuff.
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_prefix}/src
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib64/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/snort
find $RPM_BUILD_ROOT -name \*.la -exec rm -f {} \;
find $RPM_BUILD_ROOT -name \*.a -exec rm -f {} \;

mv $RPM_BUILD_ROOT%{_prefix}/lib/snort_dynamicengine \
	$RPM_BUILD_ROOT%{_prefix}/lib/snort%{version}_dynamicengine

mv $RPM_BUILD_ROOT%{_prefix}/lib/snort_dynamicpreprocessor \
	$RPM_BUILD_ROOT%{_prefix}/lib/snort%{version}_dynamicpreprocessor

# Move the Snort installed docs to a more appropriate RPM location.
mkdir -p $RPM_BUILD_ROOT/%{_docdir}
mv $RPM_BUILD_ROOT%{_prefix}/share/doc/snort \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Rename the man page.
mv $RPM_BUILD_ROOT%{_mandir}/man8/snort.8 \
	$RPM_BUILD_ROOT%{_mandir}/man8/snort%{version}.8


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_bindir}/snort-select --if-not-set %{version}


%files
%defattr(-,root,root,-)

%{_bindir}/snort%{version}
%{_bindir}/u2boat%{version}
%{_bindir}/u2spewfoo%{version}

%{_mandir}/man8/*

%attr(0755,root,root) %dir %{_prefix}/lib/snort%{version}_dynamicengine
%attr(0644,root,root) %{_prefix}/lib/snort%{version}_dynamicengine/*

%attr(0755,root,root) %dir %{_prefix}/lib/snort%{version}_dynamicpreprocessor
%attr(0644,root,root) %{_prefix}/lib/snort%{version}_dynamicpreprocessor/*

%attr(0644,root,root) %{_docdir}/%{name}-%{version}
%docdir %{_docdir}/%{name}-%{version}


%changelog
* Fri May 18 2012 Jason Ish <ish@unx.ca> - 2.9.2.3-1
- Update for Snort 2.9.2.3

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 2.9.2.2-1
- Make public
