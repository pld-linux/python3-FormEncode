#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define	module	FormEncode
Summary:	HTML form validation, generation, and convertion package
Summary(pl.UTF-8):	Moduł do walidacji, tworzenia i konwersji formularzy HTML
Name:		python3-%{module}
# keep 2.0.x here for python2 support
Version:	2.1.1
Release:	1
License:	PSF
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/project/FormEncode/
Source0:	https://files.pythonhosted.org/packages/source/f/formencode/formencode-%{version}.tar.gz
# Source0-md5:	d179386d31ae8c32e70d004dca19ac60
Patch0:		no-egg-dep.patch
URL:		http://formencode.org/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	pydoc3 >= 1:3.6
BuildRequires:	python3-dns >= 2.0.0
BuildRequires:	python3-pycountry >= 16.10.23
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FormEncode validates and converts nested structures. It allows for a
declarative form of defining the validation, and decoupled processes
for filling and generating forms.

%description -l pl.UTF-8
FormEncode służy do sprawdzania poprawności i konwersji zagnieżdżonych
struktur. Pozwala na deklaratywny sposób definiowania reguł
poprawności i niezależne od nich wypełnianie i generowanie formularzy.

%package apidocs
Summary:	API documentation for Python FormEncode module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona FormEncode
Group:		Documentation

%description apidocs
API documentation for Python FormEncode module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona FormEncode.

%prep
%setup -q -n formencode-%{version}
%patch -P0 -p1

# uses network to validate domains (with one no longer valid anyway)
%{__rm} tests/test_email.py
# validator doctests cover Email and URL validators which include DNS lookups
%{__sed} -i -e '/^modules / s/, validators//' tests/test_doctests.py

%{__sed} -i -e 's/@VERSION@/%{version}/' docs/conf.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH="$(pwd)/build-3/lib" \
%{__python3} -m pytest tests
%endif

%{?with_doc:PYTHONPATH="$(pwd)/build-3/lib" ./regen-docs}

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

find $RPM_BUILD_ROOT%{py3_sitescriptdir}/formencode/i18n -type d -maxdepth 1 | \
	%{__sed} -ne "s,$RPM_BUILD_ROOT\(.*i18n/\([a-z]\+\(_[A-Z][A-Z]\)\?\).*\),%%lang(\2) \1,p" > py3.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f py3.lang
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitescriptdir}/formencode
%{py3_sitescriptdir}/formencode/*.py
%{py3_sitescriptdir}/formencode/__pycache__
%dir %{py3_sitescriptdir}/formencode/i18n
%{py3_sitescriptdir}/formencode/javascript
%{py3_sitescriptdir}/FormEncode-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/*
%endif
