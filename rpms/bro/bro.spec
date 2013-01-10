%define realname bro

Summary:	Bro is a powerful network analysis framework
Name:		nsm-bro
Version:	2.1
Release:	2%{?dist}
License:	BSD	
URL:		http://www.bro-ids.org/
Source0:	http://www.bro-ids.org/downloads/release/%{realname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{realname}-%{version}-%{release}-root

BuildRequires:	flex bison cmake
BuildRequires:	openssl-devel file-devel libpcap-devel zlib-devel
BuildRequires:	python-devel swig

Requires:	openssl zlib python
Requires:	libpcap

%define app_prefix %{nsm_prefix}/packages/%{realname}/%{version}

%description
Bro is a powerful network analysis framework that is much different
from the typical IDS you may know.


%prep
%setup -q -n %{realname}-%{version}


%build
./configure --prefix=%{nsm_prefix} --conf-files-dir=%{nsm_prefix}/etc/bro
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{nsm_prefix}/bin/*
%{nsm_prefix}/include/*
%{nsm_prefix}/lib/*
%{nsm_prefix}/share/*
%config %{nsm_prefix}/etc/bro/*
%doc CHANGES COPYING INSTALL NEWS README VERSION


%changelog
* Wed Jan  9 2013 Jason Ish <ish@unx.ca> - 2.1-2
- Move the configuration files into etc/bro.

* Fri Jan  4 2013 Jason Ish <ish@unx.ca> - 2.1-1
- Initial Bro RPM.
