%global version_major 2021
%global version_minor 06
%global version_patch 23

Name:           EmptyEpsilon
Summary:        Spaceship bridge simulator game
Version:        %{version_major}.%{version_minor}.%{version_patch}
Release:        1%{?dist}
License:        GPLv2

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  SFML-devel >= 2.5.1
BuildRequires:  mesa-libGLU-devel >= 9.0.0
BuildRequires:  desktop-file-utils
# The following version of "glm-devel" is not currently available for Fedora 33 and older
BuildRequires:  glm-devel >= 0.9.9.8
BuildRequires:  json11-devel

ExcludeArch:    ppc64 ppc64le

URL:            http://emptyepsilon.org/
Source0:        https://github.com/daid/EmptyEpsilon/archive/EE-%{version}.zip#/EmptyEpsilon-EE-%{version}.zip
Source1:        https://github.com/daid/SeriousProton/archive/EE-%{version}.zip#/SeriousProton-EE-%{version}.zip

# The "FindJson11.cmake" file has been taken from the following project:
#   https://github.com/MASKOR/mapit/blob/master/cmake/Findjson11.cmake
# which is licensed under LGPL-3.0 License
Source2:        Findjson11.cmake



# EmptyEpsilon downstream patches:
#Patch1:

# SeriousProton downstream patches:
Patch20:        json_debundle.patch

# EmptyEpsilon upstream patches:
Patch40:        upstream_EE_001_69d93e6acd.patch
Patch41:        upstream_EE_002_872ef2667c.patch
Patch42:        upstream_EE_003_ee0cd42bfe.patch
Patch43:        upstream_EE_004_530fe32f95.patch

# SeriousProton upstream patches:
Patch60:        upstream_SP_001_32509f2db9.patch
Patch61:        upstream_SP_002_d52a1b1b61.patch
Patch62:        upstream_SP_003_ec30d87c22.patch



Recommends:     xclip

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
%setup -q -a 1 -n EmptyEpsilon-EE-%{version}

%patch20 -p1 -d SeriousProton-EE-%{version}
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch60 -p1 -d SeriousProton-EE-%{version}
%patch61 -p1 -d SeriousProton-EE-%{version}
%patch62 -p1 -d SeriousProton-EE-%{version}

# Copy CMake module for finding "json11" to the project
cp %{SOURCE2} SeriousProton-EE-%{version}/cmake/

%build
%cmake3 \
  -DSERIOUS_PROTON_DIR=SeriousProton-EE-%{version}/ \
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
* Sat Jun 26 2021 Michal Schorm <mschorm@redhat.com> - 2021.06.23-1
- Rebase to version 2021.06.23

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

