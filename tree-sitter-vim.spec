Summary:	Vimscript grammar for tree-sitter
Name:		tree-sitter-vim
Version:	0.4.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/neovim/tree-sitter-vim/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8f3d1c3319673e20b83da6c23962dc45
URL:		https://github.com/neovim/tree-sitter-vim
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ts_vim_soname	libtree-sitter-vim.so.0

%description
A tree-sitter parser for Vimscript files.

%package devel
Summary:	Header files for tree-sitter-vim
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-vim.

%package static
Summary:	Static tree-sitter-vim library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-vim library.

%package -n neovim-parser-vim
Summary:	Vim help files parser for Neovim
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-vim
Vim help files parser for Neovim.

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

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} %{_libdir}/%{ts_vim_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/vim.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libtree-sitter-vim.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{ts_vim_soname}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtree-sitter-vim.so
%{_includedir}/tree_sitter/tree-sitter-vim.h
%{_pkgconfigdir}/tree-sitter-vim.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-vim.a

%files -n neovim-parser-vim
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/vim.so
