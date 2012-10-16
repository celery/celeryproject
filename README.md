Celeryproject website
=====================

The official Celery Project website 

**Required Django apps**
- sorl-thumbnail

**Extra python packages**
- python-memcached

Rename settings.py.sample in settings.py and change DB parameters to fit your
local db configuration and also the memcache ones, used by sorl-thumbnail
library.

Than is just a Django website so run the syncdb command and everything should
works fine.

**Production server configuration**
 - **Os**: Debian 6
 - **Db**: MySQL