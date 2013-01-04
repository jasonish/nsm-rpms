%define realname pulledpork

Summary:	A Snort Rule Management Tool
Name:		nsm-pulledpork
Version:	0.6.1
Release:	1%{?dist}
License:	GPLv2	
URL:		https://code.google.com/p/pulledpork/
Source0:	https://pulledpork.googlecode.com/files/%{realname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{realname}-%{version}-%{release}-root

Requires:	perl-libwww-perl
Requires:	perl-Crypt-SSLeay
Requires:	perl-Archive-Tar

# Don't build the -debug package.
%define debug_package %{nil}


%description
A Snort rule management tool.


%prep
%setup -q -n %{realname}-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT

%__mkdir_p -m 755 $RPM_BUILD_ROOT/%{nsm_prefix}/etc/pulledpork
%__mkdir_p -m 755 $RPM_BUILD_ROOT/%{nsm_prefix}/bin
for file in etc/*; do
    %__install -m 664 $file $RPM_BUILD_ROOT/%{nsm_prefix}/etc/pulledpork
done
%__install -m 755 pulledpork.pl $RPM_BUILD_ROOT/%{nsm_prefix}/bin/pulledpork

%files
%defattr(-,root,root,-)
%{nsm_prefix}/bin/pulledpork
%config %{nsm_prefix}/etc/pulledpork/*
%doc LICENSE README doc/*


%changelog
* Fri Jan  4 2013 Jason Ish <ish@unx.ca> - 0.6.1-1
- First cut at a pulledpork package.

