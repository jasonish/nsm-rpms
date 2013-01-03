%define _prefix /opt/nsm

Name:           nsm-suricata-select
Version:        0.3
Release:        1%{?dist}
Summary:        A tool to select the default version of Suricata
Group:          NSM
License:        BSD
URL:            http://nsm-rpms.unx.ca
Source0:	suricata-select.py
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	python

%description
This is a tool to select the default version of Suricata from the NSM
packages.


%prep


%build


%install
rm -rf $RPM_BUILD_ROOT

%__mkdir_p -m0755 $RPM_BUILD_ROOT%{_bindir}
%__install -m0755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/suricata-select


%clean
rm -rf $RPM_BUILD_ROOT


%postun
if [ $1 == 0 ]; then
	# Uninstalling, remove links.
	rm -f %{_bindir}/suricata
	rm -f %{_bindir}/suricata-debug
fi


%files
%defattr(-,root,root,-)
%{_bindir}/*
%doc


%changelog
* Wed Jan  2 2013 Jason Ish <ish@unx.ca> - 0.3-1
- Handle version specific prefixes.

* Wed Aug 22 2012 Jason Ish <ish@unx.ca> - 0.2-1
- List by default.

* Wed Apr 11 2012 Jason Ish <ish@unx.ca> - 0.01-1
- Make public

