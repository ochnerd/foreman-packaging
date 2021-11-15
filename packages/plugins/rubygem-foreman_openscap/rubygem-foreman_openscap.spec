# template: foreman_plugin
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_openscap
%global plugin_name openscap
%global foreman_min_version 1.24.0

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 5.1.0
Release: 1%{?foremandist}%{?dist}
Summary: Foreman plug-in for displaying OpenSCAP audit reports
Group: Applications/Systems
License: GPLv3
URL: https://github.com/theforeman/foreman_openscap
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: scap-security-guide
# start specfile generated dependencies
Requires: foreman >= %{foreman_min_version}
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: foreman-assets >= %{foreman_min_version}
BuildRequires: foreman-plugin >= %{foreman_min_version}
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-plugin-%{plugin_name} = %{version}
# end specfile generated dependencies

# start package.json devDependencies BuildRequires
BuildRequires: %{?scl_prefix}npm(@babel/core) >= 7.7.0
BuildRequires: %{?scl_prefix}npm(@babel/core) < 8.0.0
BuildRequires: %{?scl_prefix}npm(@theforeman/builder) >= 8.4.1
BuildRequires: %{?scl_prefix}npm(@theforeman/builder) < 9.0.0
BuildRequires: %{?scl_prefix}npm(graphql-tag) >= 2.11.0
BuildRequires: %{?scl_prefix}npm(graphql-tag) < 3.0.0
BuildRequires: %{?scl_prefix}npm(graphql) >= 15.5.0
BuildRequires: %{?scl_prefix}npm(graphql) < 16.0.0
# end package.json devDependencies BuildRequires

Obsoletes: %{?scl_prefix}rubygem-scaptimony < 0.3.2-3

%description
Foreman plug-in for managing security compliance reports.


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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%foreman_bundlerd_file
%foreman_precompile_plugin -a -s

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_instdir}/db
%{gem_libdir}
%{gem_instdir}/locale
%exclude %{gem_cache}
%exclude %{gem_instdir}/package.json
%exclude %{gem_instdir}/webpack
%{gem_spec}
%{foreman_bundlerd_plugin}
%{foreman_apipie_cache_foreman}
%{foreman_apipie_cache_plugin}
%{foreman_assets_plugin}
%{foreman_webpack_plugin}
%{foreman_webpack_foreman}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Mon Nov 01 2021 Ondrej Prazak <oprazak@redhat.com> 5.1.0-1
- Update to 5.1.0

* Fri Aug 27 2021 Ondrej Prazak <oprazak@redhat.com> 5.0.0-1
- Update to 5.0.0

* Tue Jul 13 2021 Ondrej Prazak <oprazak@redhat.com> 4.3.3-1
- Update to 4.3.3

* Wed Jun 09 2021 Ondrej Prazak <oprazak@redhat.com> 4.3.2-1
- Update to 4.3.2

* Tue May 18 2021 Ondrej Prazak <oprazak@redhat.com> 4.3.0-1
- Update to 4.3.0

* Tue Apr 06 2021 Eric D. Helms <ericdhelms@gmail.com> - 4.2.0-2
- Rebuild plugins for Ruby 2.7

* Wed Feb 24 2021 Ondrej Prazak <oprazak@redhat.com> 4.2.0-1
- Update to 4.2.0

* Thu Dec 10 2020 Ondrej Prazak <oprazak@redhat.com> 4.1.2-1
- Update to 4.1.2

* Thu Dec 03 2020 Ondrej Prazak <oprazak@redhat.com> 4.1.1-1
- Update to 4.1.1

* Thu Nov 05 2020 Ondrej Prazak <oprazak@redhat.com> 4.1.0-1
- Update to 4.1.0

* Tue Sep 08 2020 Marek Hulan <mhulan@redhat.com> 4.0.3-1
- Update to 4.0.3

* Thu Aug 13 2020 Ondrej Prazak <oprazak@redhat.com> 4.0.2-1
- Update to 4.0.2

* Thu May 21 2020 Ondrej Prazak <oprazak@redhat.com> 4.0.0-1
- Update to 4.0.0

* Mon Mar 02 2020 Ondrej Prazak <oprazak@redhat.com> 3.0.0-1
- Update to 3.0.0

* Tue Jan 07 2020 Eric D. Helms <ericdhelms@gmail.com> - 2.0.2-3
- Drop migrate, seed and restart posttans

* Mon Dec 02 2019 Evgeni Golov - 2.0.2-2
- Use package names, not provides in Obsoletes

* Fri Nov 15 2019 Ondrej Prazak <oprazak@redhat.com> 2.0.2-1
- Update to 2.0.2

* Tue Nov 12 2019 Ondrej Prazak <oprazak@redhat.com> 2.0.1-1
- Update to 2.0.1

* Fri Oct 25 2019 Ondrej Prazak <oprazak@redhat.com> 2.0.0-1
- Update to 2.0.0

* Thu Sep 19 2019 Marek Hulan <mhulan@redhat.com> 1.0.8-1
- Update to 1.0.8

* Wed Sep 11 2019 Marek Hulan <mhulan@redhat.com> 1.0.7-1
- Update to 1.0.7

* Thu Sep 05 2019 Marek Hulan <mhulan@redhat.com> 1.0.6-1
- Update to 1.0.6

* Thu Aug 08 2019 Marek Hulan <mhulan@redhat.com> 1.0.5-1
- Update to 1.0.5

* Wed Jul 10 2019 Ondrej Prazak <oprazak@redhat.com> 1.0.4-1
- Update to 1.0.4

* Thu May 16 2019 Ondrej Prazak <oprazak@redhat.com> 1.0.1-1
- Update to 1.0.1

* Thu Apr 11 2019 Marek Hulan <mhulan@redhat.com> 0.12.3-1
- Update to 0.12.3

* Tue Mar 26 2019 Marek Hulan <mhulan@redhat.com> 0.12.2-1
- Update to 0.12.2

* Tue Mar 19 2019 Marek Hulan <mhulan@redhat.com> 0.12.1-1
- Update to 0.12.1

* Wed Jan 16 2019 Marek Hulan <mhulan@redhat.com> 0.11.4-1
- Update to 0.11.4

* Thu Jan 10 2019 Marek Hulan <mhulan@redhat.com> 0.11.3-1
- Update to 0.11.3

* Wed Nov 28 2018 Marek Hulan <mhulan@redhat.com> 0.11.2-1
- Update to 0.11.2

* Tue Nov 13 2018 Marek Hulan <mhulan@redhat.com> 0.11.1-1
- Update to 0.11.1

* Fri Oct 26 2018 Marek Hulan <mhulan@redhat.com> 0.11.0-1
- Update to 0.11.0

* Thu Oct 11 2018 Marek Hulan <mhulan@redhat.com> 0.10.4-1
- Update to 0.10.4

* Mon Sep 10 2018 Eric D. Helms <ericdhelms@gmail.com> - 0.10.3-2
- Rebuild for Rails 5.2 and Ruby 2.5

* Thu Sep 06 2018 Marek Hulan <mhulan@redhat.com> 0.10.3-1
- Update to 0.10.3

* Thu Jul 19 2018 Marek Hulan <mhulan@redhat.com> 0.10.2-1
- Update to 0.10.2

* Fri Jun 15 2018 Marek Hulan <mhulan@redhat.com> 0.10.1-1
- Update to 0.10.1

* Thu May 31 2018 Marek Hulan <mhulan@redhat.com> 0.9.3-1
- Update to 0.9.3

* Mon May 28 2018 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> - 0.9.2-2
- Regenerate spec file based on the current template

* Thu Jan 11 2018 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> 0.9.0-1
- Update foreman_openscap to 0.9.0 (mhulan@redhat.com)

* Thu Jan 04 2018 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> 0.8.4-1
- Updates foreman_openscap to 0.8.4 (mhulan@redhat.com)

* Fri Oct 27 2017 Daniel Lobato Garcia <me@daniellobato.me> 0.8.3-2
- Precompile assets for foreman_openscap in nightlies
  (xprazak2@users.noreply.github.com)

* Tue Oct 24 2017 Daniel Lobato Garcia <me@daniellobato.me> 0.8.3-1
- Update foreman_openscap to 0.8.3 (ares@users.noreply.github.com)

* Wed Sep 27 2017 Daniel Lobato Garcia <me@daniellobato.me> 0.8.2-1
- Update foreman_openscap to 0.8.2 (ares@users.noreply.github.com)
- Use HTTPS URLs for github and rubygems (ewoud@kohlvanwijngaarden.nl)

* Wed Sep 13 2017 Daniel Lobato Garcia <me@daniellobato.me> 0.8.1-1
- Update foreman_openscap to 0.8.1 (ares@users.noreply.github.com)
- Set proper download URLs for rubygems (komidore64@gmail.com)

* Wed Jun 28 2017 Eric D. Helms <ericdhelms@gmail.com> 0.8.0-1
- Update foreman_openscap to 0.8.0 (mhulan@redhat.com)

* Fri Jun 23 2017 Eric D. Helms <ericdhelms@gmail.com> 0.7.3-1
- Update foreman_openscap to 0.7.3 (mhulan@redhat.com)

* Wed May 31 2017 Dominic Cleal <dominic@cleal.org> 0.7.2-1
- Update foreman_openscap to 0.7.2 (mhulan@redhat.com)

* Wed Apr 05 2017 Dominic Cleal <dominic@cleal.org> 0.7.1-1
- Update foreman_openscap to 0.7.1 (mhulan@redhat.com)

* Thu Mar 30 2017 Dominic Cleal <dominic@cleal.org> 0.7.0-1
- Update foreman_openscap to 0.7.0 (mhulan@redhat.com)

* Fri Mar 24 2017 Dominic Cleal <dominic@cleal.org> 0.6.6-1
- Update foreman_openscap to 0.6.6 (mhulan@redhat.com)

* Wed Mar 15 2017 Dominic Cleal <dominic@cleal.org> 0.6.5-1
- Update foreman_openscap to 0.6.5 (mhulan@redhat.com)

* Tue Feb 21 2017 Dominic Cleal <dominic@cleal.org> 0.6.4-1
- Update foreman_openscap to 0.6.4 (mhulan@redhat.com)

* Wed Oct 19 2016 Dominic Cleal <dominic@cleal.org> 0.6.3-1
- Update foreman openscap to 0.6.3 (oprazak@redhat.com)

* Wed Sep 21 2016 Dominic Cleal <dominic@cleal.org> 0.6.2-1
- Update foreman_openscap to 0.6.2 (ares@users.noreply.github.com)

* Wed Sep 07 2016 Dominic Cleal <dominic@cleal.org> 0.6.1-1
- Update foreman_openscap to 0.6.1 (mhulan@redhat.com)

* Fri Sep 02 2016 Dominic Cleal <dominic@cleal.org> 0.6.0-1
- Update foreman_openscap to 0.6.0 (oprazak@redhat.com)
- Modernise spec file (dominic@cleal.org)

* Thu Jun 02 2016 Dominic Cleal <dominic@cleal.org> 0.5.4-1
- Version bump foreman_openscap 0.5.4 (shlomi@ben-hanna.com)

* Thu Jan 28 2016 Dominic Cleal <dcleal@redhat.com> 0.5.3-1
- foreman_openscap 0.5.3 (shlomi@ben-hanna.com)

* Thu Dec 24 2015 Dominic Cleal <dcleal@redhat.com> 0.5.2-2
- Replace ruby(abi) for ruby22 rebuild (dcleal@redhat.com)

* Thu Dec 10 2015 Dominic Cleal <dcleal@redhat.com> 0.5.2-1
- foreman_openscap version 0.5.2 (shlomi@ben-hanna.com)

* Mon Nov 02 2015 Dominic Cleal <dcleal@redhat.com> 0.5.0-1
- foreman_openscap 0.5.0 (shlomi@ben-hanna.com)
- Remove Scaptimony (shlomi@ben-hanna.com)

* Thu Aug 27 2015 Dominic Cleal <dcleal@redhat.com> 0.4.3-2
- Converted to tfm SCL (dcleal@redhat.com)

* Thu Aug 20 2015 Dominic Cleal <dcleal@redhat.com> 0.4.3-1
- Release foreman_openscap 0.4.3 (shlomi@ben-hanna.com)

* Fri Aug 14 2015 Dominic Cleal <dcleal@redhat.com> 0.4.2-1
- foreman_openscap 0.4.2 (shlomi@ben-hanna.com)
- Better branched builds with Foreman version macro (dcleal@redhat.com)

* Tue May 12 2015 Dominic Cleal <dcleal@redhat.com> 0.4.1-1
- foreman_openscap 0.4.1 (shlomi@ben-hanna.com)

* Wed Mar 25 2015 Šimon Lukašík <slukasik@redhat.com> - 0.4.0-1
- new upstream release

* Thu Mar 19 2015 Šimon Lukašík <slukasik@redhat.com> - 0.3.3-1
- new upstream release

* Mon Mar 02 2015 Šimon Lukašík <slukasik@redhat.com> - 0.3.2-1
- new upstream release
- fix FTBFS, missing foreman-plugins dep for build macros (dcleal@redhat.com)

* Thu Feb 12 2015 Šimon Lukašík <slukasik@redhat.com> - 0.3.1-1
- new upstream release

* Wed Jan 28 2015 Šimon Lukašík <slukasik@redhat.com> - 0.3.0-1
- new upstream release

* Fri Jan 23 2015 Marek Hulán <mhulan@redhat.com> - 0.2.1-1
- new upstream release

* Thu Dec 04 2014 Šimon Lukašík <slukasik@redhat.com> - 0.2.0-1
- new upstream release

* Thu Oct 23 2014 Šimon Lukašík <slukasik@redhat.com> - 0.1.0-1
- rebuilt

* Mon Jul 28 2014 Šimon Lukašík <slukasik@redhat.com> - 0.0.1-1
- Initial package