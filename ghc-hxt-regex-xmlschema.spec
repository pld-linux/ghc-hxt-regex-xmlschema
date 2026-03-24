#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hxt-regex-xmlschema
Summary:	A regular expression library for W3C XML Schema regular expressions
Summary(pl.UTF-8):	Biblioteka wyrażeń regularnych ze specyfikacji W3C XML Schema
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
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.10
BuildRequires:	ghc-hxt-charproperties >= 9
BuildRequires:	ghc-hxt-charproperties < 10
BuildRequires:	ghc-parsec >= 2.1
BuildRequires:	ghc-parsec < 4
BuildRequires:	ghc-text >= 0.10
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.10
BuildRequires:	ghc-hxt-charproperties-prof >= 9
BuildRequires:	ghc-hxt-charproperties-prof < 10
BuildRequires:	ghc-parsec-prof >= 2.1
BuildRequires:	ghc-parsec-prof < 4
BuildRequires:	ghc-text-prof >= 0.10
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4
Requires:	ghc-bytestring >= 0.10
Requires:	ghc-hxt-charproperties >= 9
Requires:	ghc-parsec >= 2.1
Requires:	ghc-text >= 0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library supports full W3C XML Schema regular expressions
inclusive all Unicode character sets and blocks. The complete grammar
can be found under <http://www.w3.org/TR/xmlschema11-2/#regexs>. It is
implemented by the technique of derivations of regular expressions.

%description -l pl.UTF-8
Ta biblioteka zawiera pełną obsługę wyrażeń regularnych ze
specyfikacji W3C XML Schema, w tym wszystkie zestawy znaków i bloki
Unicode. Kompletną gramatyke można znaleźć pod
<http://www.w3.org/TR/xmlschema11-2/#regexs>. Jest zaimplementowana z
użyciem techniki wywodów wyrażeń regularnych.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-bytestring-prof >= 0.10
Requires:	ghc-hxt-charproperties-prof >= 9
Requires:	ghc-parsec-prof >= 2.1
Requires:	ghc-text-prof >= 0.10

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

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
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

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
