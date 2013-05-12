# src:
# xfdftool.tar.bz2 (MyPkg/xfdftool.java, build.sh, build.xml, xfdftool[.sh], Makefile?)
# itext-<version>.jar
#
# 1. ./build.sh
# 2. install jar into /usr/lib/...
# 3. install sh

Name:           xfdftool
Version:	0.0.1
Release:	1%{?dist}
Summary:	XFDF tool
Group:		Development
License:	GPL
Source:		%{name}-%{version}.tar.bz2
Source1:	itextpdf-5.3.0.jar
BuildRequires:	java-sdk
Requires:	jre

%description
XFDF tool for PDF forms:
- show form fields info
- generate XFDF template
- populate form with XFDF

%prep
%setup -q
%setup -D -T -a 1

%build
javac -cp "." MyPkg/xfdftool.java
jar cmf Manifest.txt xfdftool.jar MyPkg/*.class com

%install
rm -rf %{buildroot}
%{__install} -Dpm 0644 %{name}.jar %{buildroot}%{_libdir}/%{name}/%{name}.jar
%{__install} -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{name}.jar
%{_bindir}/%{name}

%changelog
* Wed Jun 06 2012 TI_Eugene <ti.eugene@gmail.com> 0.0.1
- Initial build

