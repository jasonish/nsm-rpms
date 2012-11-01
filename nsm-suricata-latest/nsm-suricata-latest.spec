Name:           nsm-suricata-latest
Version:        1.3.3
Release:        1%{?dist}
Summary:        A pseudo package that always depends on the latest Suricata
Group:          NSM
License:        GPL
URL:            http://nsm-rpms.unx.ca
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       nsm-suricata%{version}

%description

This is a pseudo package that will always depend on the latest
available stable version of Suricata.  By installing this package that
latest version of Suricata will always be installed as it is made
available.


%prep


%build


%install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc


%changelog
* Thu Oct  4 2012 Jason Ish <ish@unx.ca> - 1.3.2-1
- Update to Suricata 1.3.2.

* Wed Aug 22 2012 Jason Ish <ish@unx.ca> - 1.3.1-1
- Update to 1.3.1

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.2-1
- Make public

