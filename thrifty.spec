Name: thrifty-gui
Version: 0.10
Release: 1%{?dist}
Summary: Utility for archiving or cleaning "rpmdb-out" files
Summary(ru): Утилита для архивирования и очистки "не-пакетных" файлов
Group: Applications/System
License: GPL2+
Source0: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://github.com/F1ash/thrifty-gui
BuildArch: noarch

Requires: python, thrifty
BuildRequires: desktop-file-utils

%description
Thrifty GUI
Utility for archiving or cleaning "rpmdb-out" files

%description -l ru
Thrifty GUI
Утилита для архивирования и очистки "не-пакетных" файлов

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/icons
install -D -m 755 -p %{name} $RPM_BUILD_ROOT/%{_bindir}/%{name}
install -D -m 644 -p *.py $RPM_BUILD_ROOT/%{_datadir}/%{name}/*
install -D -m 644 -p ./icons/* $RPM_BUILD_ROOT/%{_datadir}/%{name}/icons/*


desktop-file-install --delete-original		\
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications thrifty.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/thrifty.desktop

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/*
%{_datadir}/%{name}/BackUp.py
%{_datadir}/%{name}/Box.py
%{_datadir}/%{name}/CheckFile.py
%{_datadir}/%{name}/CleanUp.py
%{_datadir}/%{name}/ListingText.py
%{_datadir}/%{name}/MainWindow.py
%{_datadir}/%{name}/StatusBar.py
%{_datadir}/%{name}/%{name}.py
%{_datadir}/applications/thrifty.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Tue Mar 06 2012 Fl@sh <kaperang07@gmail.com> - 0.10-1
- Initial build
