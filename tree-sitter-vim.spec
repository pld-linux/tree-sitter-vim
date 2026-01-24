#
# Conditional build:
%bcond_without	python3	# Python 3.x binding

Summary:	Vimscript grammar for tree-sitter
Summary(pl.UTF-8):	Gramatyka skryptów Vima dla tree-sittera
Name:		tree-sitter-vim
Version:	0.7.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tree-sitter-grammars/tree-sitter-vim/releases
Source0:	https://github.com/neovim/tree-sitter-vim/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c267a0b056214551b5739b8693b6750d
URL:		https://github.com/neovim/tree-sitter-vim
# c11
BuildRequires:	gcc >= 6:4.7
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-wheel
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		soname_ver	0

%description
A tree-sitter parser for Vimscript files.

%description -l pl.UTF-8
Gramatyka skryptów Vima dla tree-sittera.

%package devel
Summary:	Header files for tree-sitter-vim
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tree-sitter-vim
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-vim.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tree-sitter-vim.

%package static
Summary:	Static tree-sitter-vim library
Summary(pl.UTF-8):	Statyczna biblioteka tree-sitter-vim
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-vim library.

%description static -l pl.UTF-8
Statyczna biblioteka tree-sitter-vim.

%package -n neovim-parser-vim
Summary:	Vim script files parser for Neovim
Summary(pl.UTF-8):	Analizator składni skryptów Vima dla Neovima
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-vim
Vim script files parser for Neovim.

%description -n neovim-parser-vim -l pl.UTF-8
Analizator składni skryptów Vima dla Neovima.

%package -n python3-tree-sitter-vim
Summary:	Vim script files parser for Python
Summary(pl.UTF-8):	Analizator składni skryptów Vima dla Pythona
Group:		Libraries/Python
Requires:	python3-tree-sitter >= 0.21

%description -n python3-tree-sitter-vim
Vim script files parser for Python.

%description -n python3-tree-sitter-vim -l pl.UTF-8
Analizator składni skryptów Vima dla Pythona.

%prep
%setup -q

%build
%{__make} \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} ../../libtree-sitter-vim.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/vim.so

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/tree_sitter_vim/*.c
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_libdir}/libtree-sitter-vim.so.*.*
%ghost %{_libdir}/libtree-sitter-vim.so.%{soname_ver}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-vim.so
%{_includedir}/tree_sitter/tree-sitter-vim.h
%{_pkgconfigdir}/tree-sitter-vim.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-vim.a

%files -n neovim-parser-vim
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/vim.so

%if %{with python3}
%files -n python3-tree-sitter-vim
%defattr(644,root,root,755)
%dir %{py3_sitedir}/tree_sitter_vim
%{py3_sitedir}/tree_sitter_vim/_binding.abi3.so
%{py3_sitedir}/tree_sitter_vim/__init__.py
%{py3_sitedir}/tree_sitter_vim/__init__.pyi
%{py3_sitedir}/tree_sitter_vim/py.typed
%{py3_sitedir}/tree_sitter_vim/__pycache__
%{py3_sitedir}/tree_sitter_vim/queries
%{py3_sitedir}/tree_sitter_vim-%{version}-py*.egg-info
%endif
