Summary:	Bug Tracking System
Summary(pl):	System ¶ledzenia b³êdów
Name:		flyspray
Version:	0.9.5
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://flyspray.rocks.cc/files/%{name}-%{version}.tar.gz
# Source0-md5:	efb1c68721f43aca3b47076b5da27442
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
URL:		http://flyspray.rocks.cc/
Requires:	adodb
Requires:	php
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_sysconfdir	/etc/%{name}
%define _appdir		%{_datadir}/%{name}

%description
Flyspray is an easy to use BTS for those who don't require all the
complexities of something like Bugzilla.

%description -l pl
Flyspray jest ³atwym w u¿yciu System ¦ledzenia B³êdów (ang. Bug
Tracking System - BTS) dla osób, którym nie potrzebne s± kompleksowe
rozwi±zania w stylu Bugzilla.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},/etc/httpd/httpd.conf}

install f* i* r* $RPM_BUILD_ROOT%{_appdir}
cp -r lang scripts themes $RPM_BUILD_ROOT%{_appdir}

install header.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/header.php $RPM_BUILD_ROOT%{_appdir}/header.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/httpd.conf/99_%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl graceful 1>&2
fi

%postun
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl graceful 1>&2
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CHANGELOG INSTALL README TODO UPGRADING sql
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/httpd.conf/99_%{name}.conf
%{_appdir}
