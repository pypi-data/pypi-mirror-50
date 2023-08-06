# your package information
name = "greendeck-redis"
__version__ = "0.0.4"
author = "Yashvardhan Srivastava"
author_email = "yash@greendeck.co"
url = ""

# import sub packages
from .src.redis.redis import Redis
from .src.redis.redis import RedisSet
from .src.redis.redis import RedisQueue
