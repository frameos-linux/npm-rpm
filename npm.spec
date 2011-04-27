%define __arch_install_post   /usr/lib/rpm/check-rpaths

Name:           npm
Version:        0.2.14
Release:        5%{?dist}
Summary:        A package manager for Node.js
Group:          Development/Libraries/Other
License:        MIT
URL:             http://npmjs.org/
%define realversion 0.2.14-3
Source0:        npm-v%{realversion}.tar.gz
BuildRoot:	     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: nodejs fdupes
Requires:       nodejs
BuildArch:      noarch

%description
NPM is a package manager for Node.js.
You can use it to install and publish your node programs.
It manages dependencies and does other cool stuff.

%prep
%setup -q -n npm-v%{realversion}


%clean
rm -rf %{buildroot}


%build


%install
echo "root = "%{buildroot}/usr/lib/node > $(pwd)/npmrc
echo "binroot = "%{buildroot}%{_bindir} >> $(pwd)/npmrc
echo "manroot = "%{buildroot}%{_mandir} >> $(pwd)/npmrc
echo "loglevel = verbose" >> $(pwd)/npmrc
npm_config_globalconfig=$(pwd)/npmrc node cli.js install .
rm $(pwd)/npmrc

# Replace NPM symlinks by normal files
buildroot_escaped=`echo '%{buildroot}' | sed -e 's/\\//\\\\\\//g'`
realversion_escaped=`echo '%{realversion}' | sed -e 's/\\//\\\\\\//g'`
mandir_escaped=`echo '%{_mandir}' | sed -e 's/\\//\\\\\\//g'`
rm %{buildroot}%{_mandir}/man1/*
mv %{buildroot}/usr/lib/node/.npm/npm/%{realversion}/package/man1/npm.1 %{buildroot}%{_mandir}/man1/npm.1
ls -l %{buildroot}/usr/lib/node/.npm/npm/%{realversion}/package/man1/*.1 | sed -e "s/.*\/\(.*\)$/cp ${buildroot_escaped}\/usr\/lib\/node\/.npm\/npm\/${realversion_escaped}\/package\/man1\/\1 ${buildroot_escaped}${mandir_escaped}\/man1\/npm-\1/g" | bash

rm %{buildroot}%{_bindir}/npm
mv %{buildroot}%{_bindir}/npm@%{realversion} %{buildroot}%{_bindir}/npm

rm -r %{buildroot}/usr/lib/node/npm
mv %{buildroot}/usr/lib/node/npm@%{realversion} %{buildroot}/usr/lib/node/npm

# Remove duplicates
#%fdupes -s %{buildroot}%{_datadir}

# Rudiment
rm  %{buildroot}/usr/lib/node/.npm/npm/%{realversion}/package/npmrc

#
rm -f %{buildroot}/usr/lib/node/.npm/npm/%{realversion}/package/.gitignore
chmod -x %{buildroot}/usr/lib/node/.npm/npm/%{realversion}/package/test/packages/bindir/test.js

cat %{buildroot}/usr/lib/node/npm/package.json.js | sed -e "s/${buildroot_escaped}//" > %{buildroot}/usr/lib/node/npm/package.json.js.temp
mv -f %{buildroot}/usr/lib/node/npm/package.json.js.temp %{buildroot}/usr/lib/node/npm/package.json.js


%files
%defattr(-,root,root,-)
%exclude /usr/lib/node/.npm/.cache
%dir /usr/lib/node/npm
/usr/lib/node/npm/*
%dir /usr/lib/node/.npm
/usr/lib/node/.npm/*
%attr(755,root,root) %{_bindir}/npm
%attr(755,root,root) %{_bindir}/read-package-json
%attr(755,root,root) %{_bindir}/read-package-json@%{realversion}
%attr(755,root,root) %{_bindir}/semver
%attr(755,root,root) %{_bindir}/semver@%{realversion}
%{_mandir}/man1/*


%changelog
* Wed Apr 27 2011 Sergio Rubio <rubiojr@frameos.org> - 0.2.14-5
- add dist tag to Release

* Thu Apr 07 2011 Sergio Rubio <rubiojr@frameos.org> - 0.2.14-4
- fix build defining __arch_install_post

* Mon Jan 10 2011 Oleg Efimov <efimovvo@gmail.com> 0.2.14-3
- Update NPM to 0.2.14-3
- Move changelog into npm.changes
* Thu Dec  9 2010 Oleg Efimov <efimovvo@gmail.com> 0.2.11-1
- Update NPM to 0.2.11-5
* Thu Nov 25 2010 Oleg Efimov <efimovvo@gmail.com> 0.2.9-1
- Update NPM to 0.2.9
* Wed Nov 17 2010 Oleg Efimov <efimovvo@gmail.com> 0.2.8-1
- Update NPM to 0.2.8
* Sun Nov  7 2010 Oleg Efimov <efimovvo@gmail.com> 0.2.6-1
- Update NPM to 0.2.6-1
* Sat Oct 30 2010 Oleg Efimov <efimovvo@gmail.com> 0.2.5-1
- Update NPM to 0.2.5-1
* Mon Oct 18 2010 Oleg Efimov <efimovvo@gmail.com> 0.2.4-1
- Update NPM to 0.2.4-1
- Fix some stuff for consistency with nodejs package, remove symlinks
* Sun Oct 17 2010 Alan Gutierrez <alan@blogometer.com> 0.2.2-0
- Initial RPM packaging of NPM, v0.2.2-9 included
