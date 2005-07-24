Summary:	Bug Tracking System
Summary(pl):	System ¶ledzenia b³êdów
Name:		flyspray
Version:	0.9.7
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://flyspray.rocks.cc/files/%{name}-%{version}.tar.gz
# Source0-md5:	ab686864412a0fb4590560ee360bb1f5
Source1:	%{name}.conf
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},/etc/httpd}

install *.php *.ico $RPM_BUILD_ROOT%{_appdir}
cp -r includes sql lang scripts themes $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/flyspray.conf.php
ln -sf %{_sysconfdir}/flyspray.conf.php $RPM_BUILD_ROOT%{_appdir}/flyspray.conf.php

cat > $RPM_BUILD_ROOT/etc/httpd/%{name}.conf <<EOF
Alias /%{name} %{_appdir}

<Directory %{_appdir}/sql >
    Options None
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
</Directory>	
EOF

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
%doc docs/AUTHORS.txt docs/BUGS.txt docs/CHANGELOG.txt docs/INSTALL.txt docs/README.txt docs/TODO.txt docs/UPGRADING.txt
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%{_appdir}
%exclude %{_appdir}/lang/langdiff.php
