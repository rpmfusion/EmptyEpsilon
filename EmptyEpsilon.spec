%global version_major 2021
%global version_minor 03
%global version_patch 31

%undefine __cmake_in_source_build

Name:           EmptyEpsilon
Summary:        Spaceship bridge simulator game
Version:        %{version_major}.%{version_minor}.%{version_patch}
Release:        1%{?dist}
License:        GPLv2
Recommends:     xclip
BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  SFML-devel >= 2.3.2
BuildRequires:  mesa-libGLU-devel >= 9.0.0
BuildRequires:  desktop-file-utils
ExcludeArch:    ppc64 ppc64le
URL:            http://emptyepsilon.org/
Source0:        https://github.com/daid/EmptyEpsilon/archive/EE-%{version}.zip#/EmptyEpsilon-EE-%{version}.zip
Source1:        https://github.com/daid/SeriousProton/archive/EE-%{version}.zip#/SeriousProton-EE-%{version}.zip

%description
EmptyEpsilon places you in the roles of a spaceship's bridge officers, like
those seen in Star Trek. While you can play EmptyEpsilon alone or with friends,
the best experience involves 6 players working together on each ship.

Each officer fills a unique role: Captain, Helms, Weapons, Relay, Science, and
Engineering. Except for the Captain, each officer operates part of the ship
through a specialized screen. The Captain relies on their trusty crew to report
information and follow orders.

Note: Network play require port 35666 UDP and TCP allowed in firewall.

%prep
%autosetup -b 1 -n EmptyEpsilon-EE-%{version}

%build
%cmake3 \
  -DSERIOUS_PROTON_DIR=%{_builddir}/SeriousProton-EE-%{version}/ \
  -DCPACK_PACKAGE_VERSION_MAJOR=%{version_major} \
  -DCPACK_PACKAGE_VERSION_MINOR=%{version_minor} \
  -DCPACK_PACKAGE_VERSION_PATCH=%{version_patch} \
  -DCONFIG_DIR=%{_sysconfdir}/emptyepsilon/
%cmake3_build

%install
%cmake3_install

# icon to pixmaps
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -p -m 644 ./logo.png %{buildroot}%{_datadir}/pixmaps/EmptyEpsilon.png

# .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Name=%{name}
GenericName=EmptyEpsilon
Comment=Spaceship bridge simulator game
Exec=EmptyEpsilon
Icon=EmptyEpsilon
Terminal=false
Type=Application
Categories=Game;Simulation;
EOF
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md script_reference.html
%license LICENSE
%{_bindir}/EmptyEpsilon
%{_datadir}/emptyepsilon
%{_datadir}/pixmaps/EmptyEpsilon.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Sat Apr 10 2021 Michal Schorm <mschorm@redhat.com> - 2021.03.31-1
- Rebase to version 2021.03.31

* Fri Mar 19 2021 Michal Schorm <mschorm@redhat.com> - 2021.03.16-1
- Rebase to version 2021.03.16

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2020.11.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 2020 Michal Schorm <mschorm@redhat.com> - 2020.11.23-1
- Rebase to version 2020.11.23

* Sun Nov 01 2020 Michal Schorm <mschorm@redhat.com> - 2020.08.25-1
- Rebase to version 2020.08.25

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2019.05.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2019.05.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 28 2019 Jan Kalina <honza889@gmail.com> - 2019.05.21-1
- New version of game

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2018.02.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2018.02.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2018.02.15-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 2018.02.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 6 2018 Jan Kalina <jkalina@redhat.com> - 2018.02.15-1
- New version of game

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2017.11.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Jan Kalina <jkalina@redhat.com> - 2017.11.03-1
- New version of game

* Tue Sep 5 2017 Jan Kalina <jkalina@redhat.com> - 2017.05.06-1
- New version of game, applied fixes from rpmfushion review

* Wed Feb 15 2017 Jan Kalina <jkalina@redhat.com> - 2017.01.19-3
- New package built, applied fixes from fedora review

