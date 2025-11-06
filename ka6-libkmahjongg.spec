#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		libkmahjongg
Summary:	libkmahjongg
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	f62a91fe24bc8321821cf63a92395e58
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Widgets-devel >= 5.11.1
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the library used for loading and rendering of
Mahjongg tilesets and associated backgrounds, used by KMahjongg and
KShisen.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę używaną do ładowania i wyświetlania
kafelków Mahjongga i powiązanych obrazków tła. Używana jest przez
KMahjongga i KShisen.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libKMahjongg6.so.6
%{_libdir}/libKMahjongg6.so.*.*
%{_datadir}/kmahjongglib
%{_datadir}/qlogging-categories6/libkmahjongg.categories
%{_datadir}/qlogging-categories6/libkmahjongg.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KMahjongg6
%{_libdir}/cmake/KMahjongglib6
%{_libdir}/libKMahjongg6.so
