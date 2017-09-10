%global version_major 2017
%global version_minor 05
%global version_patch 06

Name:           EmptyEpsilon
Summary:        Spaceship bridge simulator game
Version:        %{version_major}.%{version_minor}.%{version_patch}
Release:        1%{?dist}
License:        GPLv2
Recommends:     xclip
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  SFML-devel >= 2.3.2
BuildRequires:  mesa-libGLU-devel >= 9.0.0
BuildRequires:  desktop-file-utils
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
mkdir _build
cd _build
%cmake .. \
  -DSERIOUS_PROTON_DIR=%{_builddir}/SeriousProton-EE-%{version}/ \
  -DCPACK_PACKAGE_VERSION_MAJOR=%{version_major} \
  -DCPACK_PACKAGE_VERSION_MINOR=%{version_minor} \
  -DCPACK_PACKAGE_VERSION_PATCH=%{version_patch} \
  -DCONFIG_DIR=%{_sysconfdir}/emptyepsilon/
%make_build

%install
cd _build
%make_install

# auto-generated help from /usr to buildroot
mv %{buildroot}%{_prefix}/script_reference.html ../

# icon to pixmaps
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -p -m 644 ../logo.png %{buildroot}%{_datadir}/pixmaps/EmptyEpsilon.png

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
* Tue Sep 5 2017 Jan Kalina <jkalina@redhat.com> - 2017.05.06-1
- New version of game, applied fixes from rpmfushion review

* Wed Feb 15 2017 Jan Kalina <jkalina@redhat.com> - 2017.01.19-3
- New package built, applied fixes from fedora review

