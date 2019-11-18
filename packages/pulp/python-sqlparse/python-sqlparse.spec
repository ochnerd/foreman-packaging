# Created by pyp2rpm-3.3.3
%global pypi_name sqlparse

Name:           python-%{pypi_name}
Version:        0.3.0
Release:        1%{?dist}
Summary:        Non-validating SQL parser

License:        BSD
URL:            https://github.com/andialbrecht/sqlparse
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
sqlparse is a non-validating SQL parser module. It provides support for
parsing, splitting and formatting SQL statements.Visit the project page < for
additional information and documentation.**Example Usage** Splitting SQL
statements:: >>> import sqlparse >>> sqlparse.split('select * from foo; select
* from bar;') [u'select * from foo; ', u'select * from bar;'] Formatting
statements:: >>> sql...

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-setuptools
%description -n python3-%{pypi_name}
sqlparse is a non-validating SQL parser module. It provides support for
parsing, splitting and formatting SQL statements.Visit the project page < for
additional information and documentation.**Example Usage** Splitting SQL
statements:: >>> import sqlparse >>> sqlparse.split('select * from foo; select
* from bar;') [u'select * from foo; ', u'select * from bar;'] Formatting
statements:: >>> sql...

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/sqlformat
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Mon Nov 18 2019 Evgeni Golov - 0.3.0-1
- Initial package.
