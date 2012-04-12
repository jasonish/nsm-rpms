%define _prefix /opt/nsm

Name:           nsm-snort-select
Version:        0.01
Release:        1%{?dist}
Summary:        A tool to select the default version of SNORT(R).
Group:          NSM
License:        BSD
URL:            http://nsm-rpms.unx.ca
Source0:	snort-select.py
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	python

%description
This is a tool to select the default version of SNORT(R) from the NSM
packages.


%prep


%build


%install
rm -rf $RPM_BUILD_ROOT

%__mkdir_p -m0755 $RPM_BUILD_ROOT%{_bindir}
%__install -m0755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/snort-select


%clean
rm -rf $RPM_BUILD_ROOT


%postun
if [ $1 == 0 ]; then
   # Uninstalling, remove links.
   rm -f %{_bindir}/snort
   rm -f %{_prefix}/lib/snort_dynamicengine
   rm -f %{_prefix}/lib/snort_dynamicpreprocessor
fi


%files
%defattr(-,root,root,-)
%{_bindir}/*
%doc


%changelog
* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 0.01-1
- Make public
