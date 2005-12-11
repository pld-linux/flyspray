Summary:	Bug Tracking System
Summary(pl):	System ¶ledzenia b³êdów
Name:		flyspray
Version:	0.9.8
Release:	0.20
License:	GPL
Group:		Applications/WWW
Source0:	http://flyspray.rocks.cc/files/%{name}-%{version}.tar.gz
# Source0-md5:	e034c2f1638cca65c41c7cb3590e2014
Source1:	%{name}.conf
Source2:	%{name}-apache.conf
Patch0:		%{name}-PLD.patch
URL:		http://flyspray.rocks.cc/
BuildRequires:	rpmbuild(macros) >= 1.264
Requires(triggerpostun):	sed >= 4.0
Requires:	adodb
Requires:	php >= 4:4.3.0
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Flyspray is an easy to use BTS for those who don't require all the
complexities of something like Bugzilla.

%description -l pl
Flyspray jest ³atwym w u¿yciu System ¦ledzenia B³êdów (ang. Bug
Tracking System - BTS) dla osób, którym nie potrzebne s± kompleksowe
rozwi±zania w stylu Bugzilla.

%package setup
Summary:	Flyspray setup package
Summary(pl):	Pakiet do wstêpnej konfiguracji Flyspray
Group:		Applications/WWW
PreReq:		%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Flyspray installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl
Ten pakiet nale¿y zainstalowaæ w celu wstêpnej konfiguracji Flyspray po
pierwszej instalacji. Potem nale¿y go odinstalowaæ, jako ¿e
pozostawienie plików instalacyjnych mog³oby byæ niebezpieczne.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

install *.php *.ico $RPM_BUILD_ROOT%{_appdir}
cp -a includes sql lang scripts themes setup $RPM_BUILD_ROOT%{_appdir}
cp -a docs/licences $RPM_BUILD_ROOT%{_appdir}/setup

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/flyspray.conf
rm -f $RPM_BUILD_ROOT%{_appdir}/flyspray.conf.php

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post setup
chmod 660 %{_sysconfdir}/flyspray.conf

%postun setup
if [ "$1" = "0" ]; then
	chmod 640 %{_sysconfdir}/flyspray.conf
fi

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 0.9.8-0.1
if [ -f /etc/%{name}/flyspray.conf.php.rpmsave ]; then
	mv -f %{_sysconfdir}/flyspray.conf{,.rpmnew}
	mv -f /etc/%{name}/flyspray.conf.php.rpmsave %{_sysconfdir}/flyspray.conf
fi

# migrate apache2 config
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
	httpd_reload=1
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
	httpd_reload=1
fi

if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc docs/{AUTHORS,BUGS,CHANGELOG,INSTALL,README,TODO,UPGRADING}.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/flyspray.conf

%{_appdir}
%exclude %{_appdir}/lang/langdiff.php
%exclude %{_appdir}/setup

%files setup
%defattr(644,root,root,755)
%{_appdir}/setup
