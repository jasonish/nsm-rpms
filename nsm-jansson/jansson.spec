%define nsm_prefix /opt/nsm
%define nsm_bindir %{nsm_prefix}/bin
%define nsm_datadir  %{nsm_prefix}/share
%define realname jansson

Summary: Jansson is a C library for JSON.
Name: nsm-jansson
Version: 2.4
Release: 1%{?dist}
License: MIT
Group: NSM
URL: http://www.digip.org/jansson/
Source0: http://www.digip.org/jansson/releases/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}%{?version_suffix}-%{release}-root

%description 
Jansson is a C library for encoding, decoding and manipulating JSON data.


%prep
%setup -q -n %{realname}-%{version}%{?version_suffix}


%build
./configure --prefix=%{nsm_prefix}
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{nsm_prefix}/lib/*.{la,so*}
rm -rf $RPM_BUILD_ROOT%{nsm_prefix}/lib/pkgconfig


%clean
rm -rf $RPM_BUILD_ROOT


%post


%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README.rst doc/*
%{nsm_prefix}/include/*
%{nsm_prefix}/lib/*.a


%changelog
* Mon Dec 17 2012 Jason Ish <ish@unx.ca> - 2.4-1
- Initial package.

