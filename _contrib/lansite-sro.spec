%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define base lansite
%define svnrev 911

Name:		%{base}-sro
Version:	0.9.3
Release:	0
License:	GPL
Group:		Development/Languages
Summary:	LanSite-SRO django project.
URL:		http://code.google.com/p/tidjango/
Source0:	%{name}-%{version}-%{svnrev}.tar.gz
Source1:	data.sql.bz2
BuildRequires:	python-devel
Requires:	httpd
Requires:	python-memcached, python-trml2pdf, python-rtfng, python-icalendar, python-paramico, python-jinja2
Requires:	Django, django-treebeard, django-polymorphic, django-extensions
%if 0%{?centos_version}
Requires:	python-imaging, python-hashlib
%endif
BuildArch:	noarch
Prefix:		/usr
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
LanSite is Django-based buisiness core.

%package	data
Summary:	Lansite initial data
Group:		Development
Requires:	%{name}

%description	data
Initial data for LanSite-SRO.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_datadir}/%{base}
%{__cp} -R * %{buildroot}%{_datadir}/%{base}
%{__rm} -rf %{buildroot}%{_datadir}/%{base}/_contrib
%{__install} -D -m 644 _contrib/%{base}.conf %{buildroot}/etc/httpd/conf.d/%{base}.conf
%{__install} -D -m 644 _contrib/%{base}.wsgi %{buildroot}%{_datadir}/%{base}/%{base}.wsgi
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/%{base}/data.sql.bz2

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc _contrib/COPYING _contrib/INSTALL _contrib/README _contrib/TODO _contrib/local_settings.py
/etc/httpd/conf.d/%{base}.conf
%{_datadir}/%{base}

%files	data
%defattr(-,root,root,-)
%{_datadir}/%{base}/data.sql.bz2

%changelog
