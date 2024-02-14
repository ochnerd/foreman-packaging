# template: foreman_plugin
%global gem_name foreman_kernel_care
%global plugin_name kernel_care
%global foreman_min_version 1.19.0

Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 1%{?foremandist}%{?dist}
Summary: Plugin for KernelCare
License: GPLv3
URL: https://github.com/maccelf/foreman_kernel_care
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start specfile generated dependencies
Requires: foreman >= %{foreman_min_version}
BuildRequires: foreman-plugin >= %{foreman_min_version}
Requires: ruby >= 2.5.0
BuildRequires: ruby >= 2.5.0
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: foreman-plugin-%{plugin_name} = %{version}
# end specfile generated dependencies

%description
This plugin removes kernel trace and update the kernel package version if
KernelCare package is installed on host.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n  %{gem_name}-%{version}

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%foreman_bundlerd_file

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/app
%{gem_instdir}/db
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_plugin}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%posttrans
%{foreman_plugin_log}

%changelog
* Wed Feb 14 2024 Foreman Packaging Automation <packaging@theforeman.org> - 2.0.0-1
- Update to 2.0.0

* Thu Oct 26 2023 Foreman Packaging Automation <packaging@theforeman.org> 1.2.1-1
- Update to 1.2.1

* Sun Oct 01 2023 Nadja Heitmann <nadjah@atix.de> 1.2.0-2
- Update packaging

* Sun Oct 01 2023 Foreman Packaging Automation <packaging@theforeman.org> 1.2.0-1
- Update to 1.2.0

* Fri Apr 01 2022 maccelf <maxmol27@gmail.com> 1.1.1-1
- Update to 1.1.1

* Thu Oct 21 2021 maccelf <maxmol27@gmail.com> 1.0.0-1
- Add rubygem-foreman_kernel_care generated by gem2rpm using the foreman_plugin template
