Summary:	Bug Tracking System
Summary(pl):	System ¶ledzenia b³êdów
Name:		flyspray
Version:	0.9.5
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://flyspray.rocks.cc/files/%{name}-%{version}.tar.gz
# Source0-md5:	efb1c68721f43aca3b47076b5da27442
Patch0:		%{name}-config.patch
URL:		http://flyspray.rocks.cc/
Requires:	adodb
Requires:	php
Requires:	webserver
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
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},/etc/httpd}

install f* i* r* $RPM_BUILD_ROOT%{_appdir}
cp -r lang scripts themes $RPM_BUILD_ROOT%{_appdir}

install header.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/header.php $RPM_BUILD_ROOT%{_appdir}/header.php

echo "Alias /%{name} %{_datadir}/%{name}" > $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*flyspray.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/phpldapadmin.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
         ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi

if [ -f /var/lock/subsys/httpd ]; then
	%{_sbindir}/apachectl graceful 1>&2
fi

%postun
if [ "$1" = "0" ]; then
        umask 027
        if [ -d /etc/httpd/httpd.conf ]; then
            rm -f /etc/httpd/httpd.conf/99_%{name}.conf
        else
                grep -v "^Include.*flyspray.conf" /etc/httpd/httpd.conf > \
                        /etc/httpd/httpd.conf.tmp
                mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			%{_sbindir}/apachectl graceful 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CHANGELOG INSTALL README TODO UPGRADING sql
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%{_appdir}
