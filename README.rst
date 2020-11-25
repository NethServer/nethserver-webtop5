==================
nethserver-webtop5
==================

WebTop 5 is a full-featured groupware written in Java.

It's composed by three parts:

* Java web application running on Tomcat 8
* PHP implementation of Active Sync protocol
* PHP implementation of CardDAV and CalDAV protocol
* PostgreSQL database

Access to web application is forced in SSL mode.

WebTop 5 has been split in 4 different RPMs:

- webtop5: Tomcat webapp and all third-party jars, derived from a WAR. It contains all jars developed by Sonicle. This package will be updated at each
  WebTop release
- webtop5-zpush: ActiveSync implementation for WebTop, it contains PHP code from z-push project (http://z-push.org/)
- webtop5-webdav: CardDAV and CalDAV implementation for WebTop, it contains PHP code from sabre/dav project (http://sabre.io/dav/)
- nethserver-webtop5: NethServer auto-configuration for WebTop

Database
========

Configuration is saved in ``webtop`` key inside ``configuration`` database.

Available properties:

* ``ActiveSyncLog``: log level of z-push implementation. As default z-push will log only relevant errors.
* ``ActiveSyncLegactIds``: can be ``enabled`` or ``disabled``. If set to ``enabled``, use backward compatibile z-push ids to avoid device full rsync on update.
  See "Active Sync" section for more info
* ``Debug``: if set to ``true``, enable debug for the web application. Default is ``false``
* ``DefaultLocale``: default locale for WebTop users. To list available locales execute: ``/etc/e-smith/events/actions/nethserver-webtop5-locale-tz``
* ``DefaultTimezone``: default timezone for WebTop users. To list available timezones: ``JAVA_HOME=/usr/share/webtop/ java ListTimeZones``
* ``MinMemory`` and ``MaxMemory``: minimun and maximum memory of Tomcat instance. Values are expressed in MB.
* ``PublicUrl``: public URL used to publish resources for the cloud. If not set, default is ``http://<FQDN>/webtop``
* ``DavServerUrl``: Dav server URL for CalDAV and CardDAV clients configuration. If not set, default is ``https://<FQDN>/webtop-dav/server.php``
* ``DavServerLog``: log level of webtop-dav implementation. As default webtop-dav will log only relevant errors.
* ``PbxProvider``: PBX provider name
* ``PbxProviderNethvoiceWebrestUrl``: NethVoice base url for API calls, used when ``PbxProvider`` is set to ``nethvoice``
* ``DefaultToolBarIconsSize``: Default dimension of the toolbar icons, available values: ``small``, ``medium``, ``large``. Default is ``medium``
* ``RemoteCalendarAutosync``: if set to ``enabled``, it enables remote calendars auto-sync functionality. The sincronization interval can be set by user on remote calendar creation. Default is ``enabled``
* ``RemoteCalendarAutosyncOnlywhenonline``: if set to ``enabled`` the remote calendars is auto-sync only when calendar’s owner is online during the sincronization time. Default is ``disabled``
* ``RemoteCategoryAutosync``: if set to ``enabled`` , it enables remote categories auto-sync functionality. The sincronization interval can be set by user on remote category creation. Default is ``enabled``
* ``RemoteCategoryAutosyncOnlywhenonline``: if set to ``enabled`` the remote categoties is auto-sync only when category’s owner is online during the sincronization time. Default is ``disabled``
* ``VirtualHost``: set custom virtual host, e.g. `mygroupware.mydomain.it`. Virtual host can be used to access WebTop and configure ActiveSync/CalDAV/CardDAV clients

Example: ::

  webtop=configuration
      ActiveSyncLog=ERROR
      Debug=false
      DefaultLocale=en_US
      DefaultTimezone=Etc/UTC
      MaxMemory=1024
      MinMemory=512
      PublicUrl=


Configuration can be applied using the ``nethserver-webtop5-update`` event.

Reset admin password
====================

1. Access the database ::

     su - postgres -c 'psql webtop5'

2. Copy & paste the following query: ::

     UPDATE "core"."local_vault" SET "password_type"='PLAIN', "password"='admin' WHERE ("domain_id"='*') AND ("user_id"='admin');

3. Access the web interface using ``admin`` user with password ``admin``.


Troubleshooting
===============

Please note that nethserver-webtop5 is composed by many parts.
Each part has its own logs and troubleshooting best practices.

Web application
---------------

The web application logs are inside ``/var/log/webtop/webtop.log``.

Tomcat
------

Tomcat instance is managed by systemd unit called ``tomcat8@webtop``.
All logs are saved inside ``/var/lib/tomcats/webtop/logs/`` directory.
The logs are rotated daily and deletes after 2 days.

Active Sync
-----------

Active Sync is implemented using a PHP application called z-push.
All logs are inside ``/var/log/z-push/`` directory.

To inspect z-push status use: ::

    sudo -u apache scl enable rh-php72 'php /usr/share/webtop/z-push/z-push-admin.php'

It is also possibile to enable z-push debug using these commands: ::

  config setprop webtop ActiveSyncLog DEBUG
  signal-event nethserver-webtop5-update

Instead of ``DEBUG`` you can use any constant supported by z-push implementation,
but remove the ``LOGLEVEL_`` prefi.
See ``/usr/share/webtop/z-push/inc/zpush.config.php``.

You can test Active Sync using this command (please set user, password and server_name): ::
  
  curl -k -u goofy@local.neth.eu:password https://server_name/Microsoft-Server-ActiveSync

You should see an HTML output containing the string: ::

  GET not supported

Legacy ids
^^^^^^^^^^

When the ``ActiveSyncLegacyIds`` is set to ``enabled``, the z-push implementation is affected by the following limitations:

- a user can't have more than one calendar with the same name
- resources with very long names (eg. calendars) can cause synchronization problems

If such problems occur, please switch to new id implementation: ::

  config setprop webtop ActiveSyncLegacyIds disabled
  rm -rf /var/log/z-push/state/*
  signal-event nethserver-webtop5-update

Please note that after switching to new implementation, **all devices will require a full synchronization**.

CardDAV and CalDAV
------------------
CardDAV and CalDAV are implemented using a PHP application called webtop-dav.
All logs are inside ``/var/log/webtop-dav/`` directory.

It is also possibile to enable webtop-dav debug using these commands: ::

  config setprop webtop DavServerLog DEBUG
  signal-event nethserver-webtop5-update

Instead of ``DEBUG`` you can use any constant supported by ``webtop-dav`` implementation.
See ``/usr/share/webtop/webtop-dav/lib/webtop/Log.php``.

To enable ``browser-plugin`` for directory indexes of the Dav server: ::

  config setprop webtop Debug true
  signal-event nethserver-webtop5-update

Tomcat instance
===============

WebTop uses its own Tomcat instance running on port ``58080``.

The instance is launched with some special Java options,
see content of ``/etc/sysconfig/tomcat8@webtop``.

