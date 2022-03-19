#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hxt-regex-xmlschema
Summary:	A regular expression library for W3C XML Schema regular expressions
Name:		ghc-%{pkgname}
Version:	9.2.0.3
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/hxt-regex-xmlschema
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	7b875bedc63771bad57e42164387c4db
URL:		http://hackage.haskell.org/package/hxt-regex-xmlschema
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-hxt-charproperties
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-hxt-charproperties-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-hxt-charproperties
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library supports full W3C XML Schema regular expressions
inclusive all Unicode character sets and blocks. The complete grammar
can be found under http://www.w3.org/TR/xmlschema11-2/#regexs. It is
implemented by the technique of derivations of regular expressions.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-hxt-charproperties-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob/Generic
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob/Generic/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob/Generic/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema/Generic
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema/Generic/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema/Generic/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Glob/Generic/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/XMLSchema/Generic/*.p_hi
%endif
