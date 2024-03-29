-- ----------------------------
-- Update Default settings
-- ---------------------------
UPDATE "core"."settings" SET value = '' WHERE key = 'dropbox.appkey' AND service_id = 'com.sonicle.webtop.core';
UPDATE "core"."settings" SET value = '' WHERE key = 'dropbox.appsecret' AND service_id = 'com.sonicle.webtop.core';
UPDATE "core"."settings" SET value = '' WHERE key = 'googledrive.clientid' AND service_id = 'com.sonicle.webtop.core';
UPDATE "core"."settings" SET value = '' WHERE key = 'googledrive.clientsecret' AND service_id = 'com.sonicle.webtop.core';
UPDATE "core"."settings" SET value = '/usr/share/webtop/bin/' WHERE key = 'php.path' AND service_id = 'com.sonicle.webtop.core';
UPDATE "core"."settings" SET value = '587' WHERE key = 'smtp.port' AND service_id = 'com.sonicle.webtop.core';
UPDATE "core"."settings" SET value = '/usr/share/webtop/z-push' WHERE key = 'zpush.path' AND service_id = 'com.sonicle.webtop.core';

-- --------------------------------
-- Update password for admin users
-- --------------------------------
UPDATE "core"."users" SET secret = '' WHERE user_uid = '991f72dc-2b96-4340-b88f-53506b160519' AND user_id = 'admin';
UPDATE "core"."local_vault" SET password = 'admin';

-- ----------------------------
-- Set default roles
-- ----------------------------

INSERT INTO "core"."users" ("domain_id", "user_id", "type", "enabled", "user_uid", "display_name", "secret") VALUES ('NethServer', 'admins', 'G', 't', '4383a654-633e-4fb6-bf8d-7f197d9c8148', 'Admins', NULL);
INSERT INTO "core"."users" ("domain_id", "user_id", "type", "enabled", "user_uid", "display_name", "secret") VALUES ('NethServer', 'users', 'G', 't', '0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'Users', NULL);

INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.core', 'SERVICE', 'ACCESS', 'com.sonicle.webtop.calendar');
INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.core', 'SERVICE', 'ACCESS', 'com.sonicle.webtop.contacts');
INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.core', 'SERVICE', 'ACCESS', 'com.sonicle.webtop.mail');
INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.core', 'SERVICE', 'ACCESS', 'com.sonicle.webtop.tasks');
INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.core', 'SERVICE', 'ACCESS', 'com.sonicle.webtop.vfs');

INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.core', 'DEVICES_SYNC', 'ACCESS', '*');
INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.core', 'USER_PROFILE_INFO', 'MANAGE', '*');
INSERT INTO "core"."roles_permissions" ("role_uid", "service_id", "key", "action", "instance") VALUES ('0f4d4fa7-7f21-48c0-96c9-fc6d861cc8fe', 'com.sonicle.webtop.mail', 'MAILCARD_SETTINGS', 'CHANGE', '*');

-- -------------------------------------------------------------------
-- Enable synchronization of calendars, contacts and task
-- Supported values: 'O' (disabled), 'R' (read-only), 'W' (read/write)
-- -------------------------------------------------------------------
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.calendar', 'default.calendar.sync', 'W');
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.contacts', 'default.category.sync', 'W');
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.tasks', 'default.category.sync', 'W');

-- -------------------------------------------
-- Hide extra info at the bottom of login page
-- -------------------------------------------
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.core', 'login.systeminfo.hide', 'true');
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.core', 'login.webappname.hide', 'true');

-- -------------------------------------
-- Set download url for dekstop notifier
-- -------------------------------------
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.core', 'addon.notifier.url', 'http://www.nethserver.org/webtop/webtop.exe');

-- -------------------------------------------
-- Disable statistic fields in event window
-- -------------------------------------------
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.calendar', 'event.statistic.fields.visible', 'false');

-- -----------------------------
-- Set Mail grid view to compact
-- -----------------------------
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.mail', 'default.viewmode', 'compact');

-- ---------------------------
-- Enable Mail compact toolbar
-- ---------------------------
INSERT INTO "core"."settings" ("service_id", "key", "value") VALUES ('com.sonicle.webtop.mail', 'toolbar.compact', 'true');
