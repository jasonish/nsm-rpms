Name:           nsm-suricata-latest
Version:        1.4.1
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
* Fri Mar  8 2013 Jason Ish <ish@unx.ca> - 1.4.1-1
- Update to 1.4.1-1.

* Fri Dec 14 2012 Jason Ish <ish@unx.ca> - 1.4-2
- Update to 1.4-2.

* Thu Dec 13 2012 Jason Ish <ish@unx.ca> - 1.4-1
- Update to 1.4.

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 1.2-1
- Make public

