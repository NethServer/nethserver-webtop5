Summary: NethServer webtop5 configuration
Name: nethserver-webtop5
Version: 1.8.13
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-cockpit.tar.gz
Source4: ListTimeZones.java
Source5: jcharset-2.0.jar
BuildArch: noarch

Requires: nethserver-mail-server, nethserver-postgresql, nethserver-httpd
Requires: nethserver-conference
Requires: php-cli, php-pgsql
Requires: perl-libintl, perl-DBD-Pg
Requires: webtop5 >= 1.5.6, webtop5-zpush, webtop5-webdav
Requires: tomcat8, java-1.8.0-openjdk
Requires: nethserver-rh-php73-php-fpm
Requires: postgresql-contrib

BuildRequires: perl, java-1.8.0-openjdk-devel
BuildRequires: nethserver-devtools

%description
NethServer webtop configuration

%prep
%setup -q

%build
%{makedocs}
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json
mkdir -p root/var/lib/nethserver/webtop/domains/NethServer
mkdir -p root/var/lib/nethserver/webtop/domains/NethServer/images
mkdir -p root/var/lib/nethserver/webtop/domains/NethServer/temp
mkdir -p root/var/lib/nethserver/webtop/domains/NethServer/models

mkdir -p root/var/lib/tomcats/webtop/{lib,logs,temp,webapps,work}
mkdir -p root/var/log/webtop
mkdir -p root/var/lib/nethserver/webtop/backup

mkdir -p root/usr/share/webtop/bin/
mkdir -p root/usr/share/webtop/updates/pre
mkdir -p root/usr/share/webtop/updates/post/main

mkdir -p root/etc/webtop/webtop

for source in %{SOURCE4}
do
    cp $source root/usr/share/webtop
    source=`basename $source`
    javac root/usr/share/webtop/$source
    rm -f root/usr/share/webtop/$source
done

cp %{SOURCE5} root/var/lib/tomcats/webtop/lib

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

%{genfilelist} %{buildroot} \
  --file /etc/sudoers.d/webtop 'attr(0440, root, root)' \
  --dir /var/lib/nethserver/webtop 'attr(755, tomcat, tomcat)' \
  --dir /var/lib/nethserver/webtop/backup 'attr(755, postgres, postgres)' \
  --dir /var/lib/nethserver/webtop/domains 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/nethserver/webtop/domains/NethServer 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/nethserver/webtop/domains/NethServer/images 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/nethserver/webtop/domains/NethServer/temp 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/nethserver/webtop/domains/NethServer/models 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/tomcats/webtop/conf 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/tomcats/webtop/logs 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/tomcats/webtop/temp 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/tomcats/webtop/webapps 'attr(-, tomcat, tomcat)' \
  --dir /var/lib/tomcats/webtop/work 'attr(-, tomcat, tomcat)' \
  --dir /var/log/webtop 'attr(-, tomcat, tomcat)' \
  --dir /etc/webtop 'attr(-, tomcat, tomcat)' \
  --dir /etc/webtop/webtop 'attr(-, tomcat, tomcat)' \
  --file /etc/sudoers.d/50_nsapi_nethserver_webtop5 'attr(0440,root,root)' \
 > %{name}-%{version}-filelist

%post

%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%config %ghost %attr (0644,root,root) %{_sysconfdir}/httpd/conf.d/webtop.conf
%config(noreplace) %attr (0644,root,root) /etc/opt/rh/rh-php73/php-fpm.d/000-webtop.conf
%dir %{_nseventsdir}/%{name}-update
%dir /usr/share/webtop/updates/pre
%dir /usr/share/webtop/updates/post
%dir /usr/share/webtop/updates/post/main
%doc COPYING
%doc README.rst

%changelog
* Thu Apr 27 2023 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.13-1
- WebTop 5.19.6 - NethServer/dev#6736

* Mon Mar 13 2023 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.12-1
- WebTop 5.18.5 - NethServer/dev#6734

* Mon Dec 12 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.11-1
- WebTop 5.18.4 - NethServer/dev#6724

* Fri Nov 04 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.10-1
- WebTop 5.18.3 - NethServer/dev#6714

* Fri Oct 14 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.9-1
- WebTop 5.18.2 - NethServer/dev#6701

* Fri Sep 02 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.8-1
- rsync disaster recovery introduces permissions issue - Bug NethServer/dev#6691

* Tue Jul 12 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.7-1
- WebTop 5.17.5 - NethServer/dev#6684

* Wed Jul 06 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.6-1
- WebTop 5.17.4 - NethServer/dev#6683

* Fri Jul 01 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.5-1
- WebTop 5.17.3 - NethServer/dev#6674

* Wed May 18 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.4-1
- WebTop 5.16.5 - NethServer/dev#6662

* Fri Apr 22 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.3-1
- WebTop 5.16.3 - NethServer/dev#6656

* Tue Apr 12 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.2-1
  - spec: require webtop5 >= 1.4.27

* Mon Mar 21 2022 Matteo Valentini <matteo.valentini@nethesis.it> - 1.8.1-1
- WebTop 5.16.1 - NethServer/dev#6640

* Thu Feb 03 2022 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.0-1
- WebTop: use PHP 7.3 for sabredav and z-push - NethServer/dev#6632

* Thu Nov 25 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.7.10-1
- WebTop 5.14.2 - NethServer/dev#6604

* Thu Nov 11 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.9-1
- WebTop 5.14.1 - NethServer/dev#6585

* Thu Sep 16 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.8-1
- WebTop 5.13.2 - NethServer/dev#6570

* Mon Jul 26 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.7-1
- WebTop 5.13.1 - NethServer/dev#6549

* Wed Jul 21 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.6-1
-  WebTop 5.13.0 - NethServer/dev#6544

* Thu Jul 01 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.4-1
- WebTop 5.12.4 - NethServer/dev#6536

* Thu Jun 10 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.3-1
- WebTop 5.12.3 - NethServer/dev#6521

* Mon May 31 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.2-1
- WebTop 5.12.2 - NethServer/dev#6515

* Fri May 14 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.1-1
- WebTop 5.12.1 - NethServer/dev#6503

* Fri Apr 16 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.7.0-1
- WebTop 5.11.3 - NethServer/dev#6463
- WebTop: add languages in Cockpit interface - NethServer/dev#6441

* Thu Mar 11 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.16-1
- WebTop 5.10.5 - NethServer/dev#6453

* Thu Feb 25 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.15-1
- WebTop 5.10.4 - NethServer/dev#6440

* Mon Feb 22 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.14-1
- WebTop 5.10.3 - NethServer/dev#6431
  - spec: require webtop5 >= 1.4.13

* Thu Feb 11 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.11-1
- WebTop 5.10.2 - NethServer/dev#6418

* Fri Jan 29 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.10-1
- Webtop 5.10.1 - NethServer/dev#6402
  - spec: require webtop5 >= 1.4.11

* Mon Jan 18 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.9-1
- WebTop: wrong URL and logo if virtual host is enabled - Bug NethServer/dev#6398

* Thu Jan 14 2021 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.8-1
- Webtop 5.10.0 - NethServer/dev#6368

* Mon Dec 07 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.7-1
- Webtop 5.9.5 - NethServer/dev#6338
  - httpd: set timeout to 180 for `/webtop` ProxyPass

* Fri Oct 09 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.6-1
- nethserver-webtop5: update UI javascript dependencies - NethServer/dev#6280

* Fri Sep 18 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.5-1
- WebTop: Virtual Host support - NethServer/dev#6241

* Mon Jul 06 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.4-1
- WebTop: automatic restart of tomcat8@webtop service on failure - NethServer/dev#6220

* Thu Jul 02 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.3-1
- Human readable numbers in Cockpit dashboards - NethServer/dev#6206

* Fri May 29 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.2-1
- WebTop 5.8.5 - NethServer/dev#6181

* Tue May 19 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.1-1
  - Update catalina.policy (#79)

* Mon Mar 23 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.6.0-1
  Delegate SMTP configuration to WebTop UI - NethServer/dev#6080
  WebTop 5.8.3 - NethServer/dev#6079

* Wed Mar 04 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.5.2-1
- WebTop 5.8.1 - NethServer/dev#6060
  - Move log config inside webtop.properties
  - Add webtop config dir

* Fri Feb 07 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.1-1
- Webtop: separate admin users to standard users - Bug Nethserver/dev#6051

* Wed Jan 08 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- Webtop 5: the SMTP STARTTLS value is changed even if not required - Bug NethServer/dev#6018
- Cockpit: add WebTop 5 interface - NethServer/dev#6003
- Cockpit: change package Dashboard page title - NethServer/dev#6004

* Tue Jan 07 2020 Matteo Valentini <matteo.valentini@nethesis.it> - 1.4.4-1
- WebTop 5.7.7 - NethServer/dev#5985
  - systemd: redirect catalina output to stdout
  - Fix systemd drop-in path

* Mon Dec 09 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.3-1
- Inventory: add new application facts - NethServer/dev#5979

* Tue Dec 03 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.2-1
- WebTop 5.7.5 - NethServer/dev#5928

* Thu Nov 07 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.1-1
- WebTop 5.7.4 - NethServer/dev#5903

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.0-1
- WebTop: new ActiveSync implementation - NethServer/dev#5732
- Cockpit legacy apps implementation - NethServer/dev#5782
- WebTop 5.7.3 - NethServer/dev#5770
- Cockpit. List correct application version - Nethserver/dev#5819
- Sudoers based authorizations for Cockpit UI - NethServer/dev#5805

* Tue Jun 25 2019 Matteo Valentini <matteo.valentini@nethesis.it> - 1.3.0-1
- WebTop 5.7.1 - NethServer/dev#5770
  - config: set default contacts ordering by last name
  - templates: enable optimized frontend javascripts
  - pst2webtop_card.php: add display_name field
  - config: enable compact toolbar as default
  - configs: Set mail grid view to compact as default

* Tue Mar 26 2019 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.19-1
- WebTop: no icon on mail attachments - Bug NethServer/dev#5731

* Fri Feb 15 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.18-1
- WebTop: incorrect PST contacts/calendars import - NethServer/dev#5709

* Fri Jan 18 2019 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.17-1
 - nethserver-webtop5-conf: fix action always failed

* Thu Dec 20 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.16-1
- Revert "z-push: use DefaultTimezone prop for set time zone"

* Mon Dec 17 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.15-1
-  WebTop 5.5.0 - NethServer/dev#5666

* Mon Dec 03 2018 Davide Principi <davide.principi@nethesis.it> - 1.2.14-1
- WebTop: use Apache Tomcat 8.5 - NethServer/dev#5638
- nethserver-webtop5:  data backup is not restored correctly - Bug NethServer/dev#5650

* Thu Nov 22 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.13-1
- WebTop 5.4.5 - NethServer/dev#5651

* Wed Nov 21 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.12-1
- nethserver-webtop5:  data backup is not restored correctly - Bug NethServer/dev#5650

* Mon Nov 05 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.11-1
- WebTop 5.4.3 - NethServer/dev#5622

* Wed Oct 24 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.10-1
- WebTop 5.4.2 - NethServer/dev#5615

* Wed Oct 17 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.9-1
- WebTop 5.4.1 - NethServer/dev#5607

* Fri Oct 12 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.8-1
- nethserver-webtop5: new release with minors fixes - NethServer/dev#5602
- Package nethserver-X must subscribe nethserver-sssd-save - NethServer/dev#5600

* Wed Sep 19 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.7-1
- WebTop 5.3.3 - NethServer/dev#5571
- spec: include JCharset 2.0 jar in rpm
- config: add remote calendar/categories autosync options
- config: add smtp auth options
- config: add toolbar icons size  option

* Wed Aug 29 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.6-1
- webtop5-zpush: Incorrect creation of calendar events and contacts. - Bug NethServer/dev#5570
- suppress Java 8 warnings

* Mon Aug 06 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.5-1
- WebTop 5: can't authenticate to local AD - Bug NethServer/dev#5560

* Tue Jul 17 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.4-1
- WebTop 5.2.3 - NethServer/dev#5516

* Thu May 17 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.3-1
- WebTop 5.1.9 - NethServer/dev#5487

* Thu Apr 26 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.2-1
- WebTop 5.1.8 - NethServer/dev#5463

* Wed Feb 21 2018 Matteo Valentini <matteo.valentini@nethesis.it> - 1.2.1-1
- WebTop 5.1.7 - NethServer/dev#5423

* Tue Jan 30 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.0-1
- WebTop 5.1.5 - NethServer/dev#5414

* Tue Jan 09 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.7-1
- WebTop 5: installation fails on ext4 - NethServer/dev#5405

* Wed Nov 29 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.6-1
- WebTop 5.1.4 - NethServer/dev#5376

* Fri Oct 06 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.5-1
- db: handle multiline encrypted password - NS 7.4

* Fri Sep 08 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.4-1
- WebTop 5.0.13 - NethServer/dev#5338
- Disable iCal4j timezone update
- Avoid automatic deploy for future releases

* Mon Sep 04 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.3-1
- WebTop 5.0.13 - NethServer/dev#5338

* Thu Jul 27 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.2-1
- WebTop5: Outlook PST import - NethServer/dev#5244

* Thu Jun 22 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.1-1
- WebTop 5.0.7 - NethServer/dev#5312
- Implement log rotation with logrotate
- Clear Tomcat cache dir on service restart

* Wed May 17 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.0-1
- WebTop 5: enable folder sorting - NethServer/dev#5275
- Build RPM from source

* Mon Mar 27 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.3-1
- WebTop 5: upgrade to RC6 - NethServer/dev#5250
- WebTop5: extended time format not set - Bug NethServer/dev#5254

* Tue Mar 14 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1
- WebTop5: can't access with master user NethServer/dev#5239

* Thu Mar 09 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.1-1
- WebTop 5: contacts don't work at all - Bug NethServer/dev#5237

* Wed Mar 08 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- WebTop 5 - NethServer/dev#5225

