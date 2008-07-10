Summary:	Bug Tracking System
Summary(pl.UTF-8):	System śledzenia błędów
Name:		flyspray
Version:	0.9.9.5.1
Release:	0.2
License:	GPL
Group:		Applications/WWW
# Source0Download: http://flyspray.org/download
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	a0181d1798cf305c1472d43797a39078
Source1:	%{name}.conf
Source2:	%{name}-apache.conf
Patch0:		%{name}-PLD.patch
URL:		http://flyspray.org/
BuildRequires:	rpmbuild(macros) >= 1.461
BuildRequires:	unzip
Requires(triggerpostun):	sed >= 4.0
Requires:	adodb >= 4.67-1.17
Requires:	php-xml
Requires:	webapps
Requires:	webserver(alias)
Requires:	webserver(access)
Requires:	webserver(indexfile)
Requires:	webserver(php) >= 4.3.0
Suggests:	php-mysql
Suggests:	php-mysqli
Suggests:	php-pgsql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Flyspray is an easy to use BTS for those who don't require all the
complexities of something like Bugzilla.

%description -l pl.UTF-8
Flyspray jest łatwym w użyciu System Śledzenia Błędów (ang. Bug
Tracking System - BTS) dla osób, którym nie potrzebne są kompleksowe
rozwiązania w stylu Bugzilla.

%package setup
Summary:	Flyspray setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Flyspraya
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Flyspray installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji Flyspraya
po pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%package lang-pl
Summary:	Flyspray Polish resource files
Summary(pl.UTF-8):	Pakiet z polską wersją językową do Flyspray
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description lang-pl
This package contains Polish localization files for Flyspray.

%description lang-pl -l pl.UTF-8
Pakiet zawiera polską lokalizację dla Flyspray'a.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

install *.php *.ico $RPM_BUILD_ROOT%{_appdir}
cp -a attachments cache includes javascript lang plugins scripts templates themes setup $RPM_BUILD_ROOT%{_appdir}
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

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 0.9.8-3.3
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
	%service httpd reload
fi

%{__sed} -i -e 's,%{php_pear_dir}/adodb/adodb.inc.php,%{php_data_dir}/adodb/adodb.inc.php,' %{_sysconfdir}/flyspray.conf

%files
%defattr(644,root,root,755)
%doc docs/{AUTHORS,BUGS,CHANGELOG,INSTALL,README,TODO,UPGRADING}.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/flyspray.conf

%{_appdir}
%exclude %{_appdir}/setup

%files setup
%defattr(644,root,root,755)
%{_appdir}/setup
