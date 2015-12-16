%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name sdoc

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.4.1
Release: 1%{?dist}
Summary: RDoc generator to build searchable HTML documentation for Ruby code
Group: Development/Languages
# License needs to take RDoc and Darkfish into account apparantly
# https://github.com/voloko/sdoc/issues/27
# SDoc itself is MIT, RDoc part is GPLv2 and Darkfish is BSD
License: MIT and GPLv2 and BSD
URL: http://github.com/voloko/sdoc
# Let's build the gem on the latest stable release to avoid confusion
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Man pages
# https://github.com/voloko/sdoc/pull/49
Source1: sdoc.1
Source2: sdoc-merge.1
# Fix sdoc --version to return the correct version
Patch0: rubygem-sdoc-version-option-fix.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}rubygem(rdoc) => 4.0
Requires: %{?scl_prefix_ruby}rubygem(rdoc) < 5
Requires: %{?scl_prefix_ruby}rubygem(json) >= 1.7.7
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}-%{release}

%description
SDoc is simply a wrapper for the rdoc command line tool.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%patch0 -p1

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

# Install man pages into appropriate place.
mkdir -p %{buildroot}%{_mandir}/man1
mv %{SOURCE1} %{buildroot}%{_mandir}/man1
mv %{SOURCE2} %{buildroot}%{_mandir}/man1

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
find %{buildroot}%{gem_instdir}/lib/rdoc/generator/template -type f | xargs chmod a-x

%check
pushd .%{gem_instdir}
# Get rid of Bundler
sed -i "s/require 'bundler\/setup'//" ./spec/spec_helper.rb

%{?scl:scl enable %{scl} - << \EOT}
# To run the tests using minitest 5
ruby -rminitest/autorun -Ilib - << \EOF
  Test = Minitest
  Dir.glob "./spec/*.rb", &method(:require)
EOF
%{?scl:EOT}
popd

%files
%dir %{gem_instdir}
%{_bindir}/sdoc
%{_bindir}/sdoc-merge
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{_mandir}/man1/sdoc-merge.1*
%doc %{_mandir}/man1/sdoc.1*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Mon Aug 18 2014 Josef Stribny <jstribny@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 0.4.0-4
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Mon Jan 27 2014 Vít Ondruch <vondruch@redhat.com> - 0.4.0-3
- Fix ruby200 scl dependencies.

* Fri Jan 24 2014 Josef Stribny <jstribny@redhat.com> - 0.4.0-2
- Fix disttag

* Mon Nov 25 2013 Josef Stribny <jstribny@redhat.com> - 0.4.0-1
- Update to sdoc 0.4.0
- Run tests
- Fix changelog

* Mon Nov 25 2013 Josef Stribny <jstribny@redhat.com> - 0.4.0-2.rc1
- Convert to scl

* Wed Nov 06 2013 Josef Stribny <jstribny@redhat.com> - 0.4.0-1.rc1
- sdoc 0.4.0 git pre-release to support RDoc 4.0

* Tue Aug 06 2013 Josef Stribny <jstribny@redhat.com> - 0.3.20-2
- Add man pages

* Tue Jul 30 2013 Josef Stribny <jstribny@redhat.com> - 0.3.20-1
- Initial package
