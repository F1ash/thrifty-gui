Name: thrifty-gui
Version: 0.20
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
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/thrifty/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/thrifty/icons/
install -D -m 755 -p %{name} $RPM_BUILD_ROOT/%{_bindir}/%{name}
install -D -m 644 -p *.py $RPM_BUILD_ROOT/%{_datadir}/thrifty/
install -D -m 644 -p icons/* $RPM_BUILD_ROOT/%{_datadir}/thrifty/icons/
install -D -m 644 -p icons/gas_soldier.png $RPM_BUILD_ROOT/%{_datadir}/pixmaps/thrifty.png

desktop-file-install --delete-original		\
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications thrifty.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/thrifty.desktop

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{_datadir}/thrifty/icons
%{_datadir}/thrifty/icons/*
%{_datadir}/thrifty/BackUp.py*
%{_datadir}/thrifty/Box.py*
%{_datadir}/thrifty/CheckFile.py*
%{_datadir}/thrifty/CleanUp.py*
%{_datadir}/thrifty/ListingText.py*
%{_datadir}/thrifty/MainWindow.py*
%{_datadir}/thrifty/Editor.py*
%{_datadir}/thrifty/StatusBar.py*
%{_datadir}/thrifty/BrokenSearch.py*
%{_datadir}/thrifty/saveHelper.py*
%{_datadir}/thrifty/%{name}.py*
%{_datadir}/applications/thrifty.desktop
%{_datadir}/pixmaps/thrifty.png

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Tue Mar 13 2012 Fl@sh <kaperang07@gmail.com> - 0.20-1
- version updated

* Tue Mar 07 2012 Fl@sh <kaperang07@gmail.com> - 0.15-1
- version updated

* Tue Mar 06 2012 Fl@sh <kaperang07@gmail.com> - 0.10-1
- Initial build
