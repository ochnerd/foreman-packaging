# template: scl
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name netbox-client-ruby
%global gem_require_name %{gem_name}

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.5.6
Release: 1%{?dist}
Summary: A read/write client for Netbox v2
Group: Development/Languages
License: MIT
URL: https://github.com/ninech/netbox-client-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
#Based on https://github.com/ninech/netbox-client-ruby/commit/ce27df12d7464145a0ce9b9f6490cfe9988035d7.patch
Patch0: remove-openssl-runtime-dependency.patch

# start specfile generated dependencies
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(dry-configurable) >= 0.1
Requires: %{?scl_prefix}rubygem(dry-configurable) < 1
Requires: %{?scl_prefix}rubygem(faraday) >= 0.11.0
Requires: %{?scl_prefix}rubygem(faraday) >= 0.11
Requires: %{?scl_prefix}rubygem(faraday) < 1
Requires: %{?scl_prefix}rubygem(faraday-detailed_logger) >= 2.1
Requires: %{?scl_prefix}rubygem(faraday-detailed_logger) < 3
Requires: %{?scl_prefix}rubygem(faraday_middleware) >= 0.11
Requires: %{?scl_prefix}rubygem(faraday_middleware) < 1
Requires: %{?scl_prefix}rubygem(ipaddress) >= 0.8
Requires: %{?scl_prefix}rubygem(ipaddress) < 1
Requires: %{?scl_prefix}rubygem(ipaddress) >= 0.8.3
# Removed as dependency see Patch0
#Requires: %%{?scl_prefix}rubygem(openssl) >= 2.0
#Requires: %%{?scl_prefix}rubygem(openssl) < 3
#Requires: %%{?scl_prefix}rubygem(openssl) >= 2.0.5
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
# end specfile generated dependencies

%description
A read/write client for Netbox v2.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}
%patch0 -p 1

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.github
%exclude %{gem_instdir}/.gitignore
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/VERSION
%{gem_instdir}/bin
%exclude %{gem_instdir}/dump.sql
%{gem_libdir}
%exclude %{gem_instdir}/netbox-client-ruby_rsa
%exclude %{gem_instdir}/netbox-client-ruby_rsa.pub
%exclude %{gem_instdir}/netbox.env
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/.dockerignore
%exclude %{gem_instdir}/.rspec
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/docker-compose.test.yml
%doc %{gem_instdir}/docker-compose.yml
%doc %{gem_instdir}/docker
%doc %{gem_instdir}/Dockerfile
%{gem_instdir}/netbox-client-ruby.gemspec

%changelog
* Tue May 31 2022 Dirk Goetz <dirk.goetz@netways.de> 0.5.6-1
- Add rubygem-netbox-client-ruby generated by gem2rpm using the scl template

