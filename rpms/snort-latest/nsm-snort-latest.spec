Name:           nsm-snort-latest
Version:        2.9.4
Release:        2%{?dist}
Summary:        A pseudo package that always depends on the latest SNORT(R).
Group:          NSM
License:        GPLv2
URL:            http://nsm-rpms.unx.ca
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       nsm-snort%{version}

%description
This is a pseudo package that will always depend on the latest
available version of SNORT(R).  By installing this package that latest
version of Snort will always be installed as it is made available.


%prep


%build


%install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc


%changelog
* Thu Jan  3 2013 Jason Ish <ish@unx.ca> - 2.9.4-2
- Don't depend on a specific release of package, yum will take care of
  getting us the latest release.

* Tue Dec  4 2012 Jason Ish <ish@unx.ca> - 2.9.4-1
- Update to Snort 2.9.4.

* Thu Aug  9 2012 Jason Ish <ish@unx.ca> - 2.9.3.1-1
- Update to Snort 2.9.3.1

* Mon Jul 30 2012 Jason Ish <ish@unx.ca> - 2.9.3-1
- Update to Snort 2.9.3

* Fri May 18 2012 Jason Ish <ish@unx.ca> - 2.9.2.3-1
- Update to Snort 2.9.2.3

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 2.9.2.2-1
- Make public

