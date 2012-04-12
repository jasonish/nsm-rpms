Name:           nsm-snort-latest
Version:        2.9.2.2
Release:        1%{?dist}
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
* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 2.9.2.2-1
- Make public

