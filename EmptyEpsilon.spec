%global version_major 2024
%global version_minor 12
%global version_patch 08

Name:           EmptyEpsilon
Summary:        Spaceship bridge simulator game
Version:        %{version_major}.%{version_minor}.%{version_patch}
Release:        2%{?dist}
# Apache-2.0, BSD-3-Clause and Zlib are used in basis_universal
# MIT is used by meshoptimizer and GLM
License:        GPL-2.0-only AND Apache-2.0 AND BSD-3-Clause AND Zlib AND MIT

BuildRequires:  cmake
BuildRequires:  dos2unix
BuildRequires:  gcc-c++
BuildRequires:  SFML-devel >= 2.5.1
BuildRequires:  mesa-libGLU-devel >= 9.0.0
BuildRequires:  desktop-file-utils
%if 0%{?fedora} < 41
BuildRequires:  glm-devel >= 0.9.9.8
%endif
BuildRequires:  SDL2-devel

ExcludeArch:    %{power64}

URL:            http://emptyepsilon.org/
Source0:        https://github.com/daid/EmptyEpsilon/archive/EE-%{version}/EmptyEpsilon-EE-%{version}.tar.gz
Source1:        https://github.com/daid/SeriousProton/archive/EE-%{version}/SeriousProton-EE-%{version}.tar.gz

# Upstream wants to download following libraries; we need to bundle them
Source2:        https://github.com/BinomialLLC/basis_universal/archive/refs/tags/v1_15_update2/basis_universal-1_15_update2.tar.gz
Source3:        https://github.com/zeux/meshoptimizer/archive/refs/tags/v0.16/meshoptimizer-0.16.tar.gz

# EmptyEpsilon is not compatible with GLM-1.0.1 yet
Source4:        https://github.com/g-truc/glm/archive/refs/tags/0.9.9.8.tar.gz

Patch0:         EmptyEpsilon-avoid_basis_libs_downloading.patch
Patch1:         EmptyEpsilon-avoid_meshoptimizer_libs_downloading.patch
Patch2:         EmptyEpsilon-avoid_glm_libs_downloading.patch

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
%autosetup -a 1 -n EmptyEpsilon-EE-%{version} -N

# basis
%patch -P 0 -p1 -b .backup_basis
%if 0%{?fedora} > 40
%patch -P 2 -p1 -b .backup_glm
%endif
pushd SeriousProton-EE-%{version}/libs/basis_universal
tar -xf %{SOURCE2}
mv basis_universal-1_15_update2 basis
mv basis/LICENSE basis/basis-LICENSE
# Use CMakeLists.txt from EmptyEpsilon upstream to compile 'basis' static library
cp -p CMakeLists.txt basis/
popd

# GLM
%if 0%{?fedora} > 40
tar -xf %{SOURCE4}
mv glm-0.9.9.8 glm
mv glm/copying.txt glm/glm-copying.txt
mv glm SeriousProton-EE-%{version}/
%endif

# meshoptimizer
tar -xf %{SOURCE3}
mv meshoptimizer-0.16 meshoptimizer
mv meshoptimizer/LICENSE.md meshoptimizer/meshoptimizer-LICENSE.md
%patch -P 1 -p1 -b .backup

%build
%global __cmake_in_source_build 1
pushd SeriousProton-EE-%{version}/libs/basis_universal/basis
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
%cmake
%cmake_build
popd

export CXXFLAGS="%{optflags} -I../SeriousProton-EE-%{version}/libs/basis_universal/basis"
export LDFLAGS="%{__global_ldflags} -L../SeriousProton-EE-%{version}/libs/basis_universal/basis"
%cmake \
  -DSERIOUS_PROTON_DIR=SeriousProton-EE-%{version}/ \
  -DCPACK_PACKAGE_VERSION_MAJOR=%{version_major} \
  -DCPACK_PACKAGE_VERSION_MINOR=%{version_minor} \
  -DCPACK_PACKAGE_VERSION_PATCH=%{version_patch} \
%if 0%{?fedora} > 40
  -DWITH_GLM="bundled" \
%else
  -DWITH_GLM="system" \
%endif
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DCONFIG_DIR=%{_sysconfdir}/emptyepsilon/

%cmake_build

%install
%cmake_install

rm -f %{buildroot}%{_datadir}/emptyepsilon/scripts/.gitignore

install -pm 644 README.md CHANGELOG.md %{buildroot}%{_docdir}/%{name}/

# icon to pixmaps
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -p -m 644 ./logo.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%files
%license LICENSE meshoptimizer/meshoptimizer-LICENSE.md
%license SeriousProton-EE-%{version}/libs/basis_universal/basis/basis-LICENSE
%if 0%{?fedora} > 40
%license SeriousProton-EE-%{version}/glm/glm-copying.txt
%endif
%{_bindir}/%{name}
%{_datadir}/emptyepsilon
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/metainfo/io.github.daid.%{name}.metainfo.xml
%{_datadir}/icons/hicolor/512x512/apps/io.github.daid.%{name}.png
%{_datadir}/applications/io.github.daid.%{name}.desktop
%{_docdir}/%{name}

%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2024.12.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Michal Schorm <mschorm@redhat.com> - 2024.12.08-1
- Rebase to 2024.12.08

* Sun Aug 11 2024 Michal Schorm <mschorm@redhat.com> - 2024.08.09-1
- Rebase to 2024.08.09

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2023.06.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 10 2024 Antonio Trande <sagitter@fedoraproject.org> - 2023.06.17-1
- Release 2023.06.17

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2021.06.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 11 2023 Leigh Scott <leigh123linux@gmail.com> - 2021.06.23-6
- Build bundled libjson11 as a static lib

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2021.06.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2021.06.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2021.06.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2021.06.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

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
