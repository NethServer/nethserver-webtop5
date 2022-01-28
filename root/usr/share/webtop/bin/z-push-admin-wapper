#!/bin/bash

# Enable SCL env
source /opt/rh/rh-php73/enable

# z-push search for config.json in current dir
cd /usr/share/webtop/z-push/

# Remove dirty arguments
shift

# SCL add "#!/usr/bin/env php" to the output, remove it with an hack
php z-push-admin.php $@ | grep -v "/usr/bin/env"
