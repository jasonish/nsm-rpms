%define _defaultdocdir %{nsm_prefix}/share/doc

%define realname netsniff-ng
%define nsm_prefix /opt/nsm

Summary: netsniff-ng is a free, performant Linux networking toolkit. 
Name: nsm-netsniff-ng
Version: 0.5.7
Release: 1%{?dist}
License: GPLv2
Group: NSM
URL: http://netnsiff-ng.org/
Source0: http://pub.netsniff-ng.org/netsniff-ng/%{realname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires: cmake, flex, bison
BuildRequires: libnl-devel
BuildRequires: libnetfilter_conntrack-devel
BuildRequires: GeoIP-devel

Requires: libnl
Requires: libnetfilter_conntrack
Requires: GeoIP

# libcli is only available on Fedora right now.
%if 0%{?fedora}
BuildRequires: libcli-devel
Requires: libcli
%endif

%description
netsniff-ng is a free, performant Linux networking toolkit. 


%prep
%setup -q -n %{realname}-%{version}


%build

# On the fly patching.
find . -type f -print0 | \
     xargs -0 perl -pi -e 's/\/etc\/netsniff-ng/\/opt\/nsm\/etc\/netsniff-ng/g'

mkdir build
pushd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{nsm_prefix} ../src
make


%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT

# Now manually move the stuff into the NSM prefix that doesn't get
# handled by -DCMAKE_INSTALL_PREFIX.
mkdir -p $RPM_BUILD_ROOT/%{nsm_prefix}
mv $RPM_BUILD_ROOT/usr/sbin $RPM_BUILD_ROOT/%{nsm_prefix}/bin


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{nsm_prefix}/bin/*
%{nsm_prefix}/share/man/man8/*
%config %{nsm_prefix}/etc/*
%doc AUTHORS COPYING README INSTALL REPORTING-BUGS VERSION Documentation/*


%changelog
* Fri Jan  4 2013 Jason Ish <ish@unx.ca> - 0.5.7-1
- First cut at a netsniff-ng package.

