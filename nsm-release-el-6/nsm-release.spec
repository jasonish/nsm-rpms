Name: nsm-release-el
Version: 6
Release: 1%{?dist}
Summary: NSM Packages for Enterprise Linux and EL Like Systems
Group: System Environment/Base 
License: Freeware
URL: http://nsm-rpms.unx.ca/
Source0: RPM-GPG-KEY-nsm
Source1: nsm.repo	

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Should limit us to only being installed on EL6.
BuildArch: noarch
Requires: redhat-release >= %{version} 
Conflicts: fedora-release

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
* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 6-1
- Make public

