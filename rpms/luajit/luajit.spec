%define realname LuaJIT

Name:		nsm-luajit
Version:	2.0.0
Release:	1%{?dist}
Summary:	A Just-In-Time Compiler for Lua.
License:	MIT
URL:		http://luajit.org/
Source0:	http://luajit.org/download/%{realname}-%{version}.tar.gz


%description
A Just-In-Time Compiler for Lua.


%prep
%setup -q -n %{realname}-%{version}


%build
make PREFIX=%{nsm_prefix}


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{nsm_prefix} DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{nsm_prefix}/*
%doc COPYRIGHT README


%changelog
* Thu Jan 10 2013 Jason Ish <ish@unx.ca> - 2.0.0-1
- Initial package of luajit.

