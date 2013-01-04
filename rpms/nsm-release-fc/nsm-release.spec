Name: nsm-release-fc
Version: 17
Release: 1%{?dist}
Summary: NSM Packages for Fedora Linux
Group: System Environment/Base 
License: BSD
URL: http://nsm-rpms.unx.ca/
Source0: RPM-GPG-KEY-nsm
Source1: nsm.repo	

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
Requires: fedora-release >= %{version}


%description
This package contains the YUM repository information for the NSM
packages for Enterprise Linux.


%prep


%build


%install
rm -rf $RPM_BUILD_ROOT

# Create directories.
install -d -m0755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -d -m0755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

# The GPG key.
%{__install} -Dp -m0644 %{SOURCE0} \
	$RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/

# The yum repo file.
%{__install} -p -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/


%clean
rm -rf $RPM_BUILD_ROOT


%post


%postun 


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Fri Apr 13 2012 Jason Ish <ish@unx.ca> - 6-2
- Depend on epel-release

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 6-1
- Make public

