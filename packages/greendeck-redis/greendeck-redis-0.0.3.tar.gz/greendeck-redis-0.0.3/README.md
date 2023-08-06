greendeck-redis
---
**For internal ```Greendeck``` use only.**

![Greendeck][gd]  ![redis][redis]

[gd]: https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/gd_transparent_blue_bg.png "Logo Title Text 2"
[redis]: https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/redis.png "Logo Title Text 2"
### Install from pip
https://pypi.org/project/greendeck-redis/

```pip install greendeck-redis```

### How to use ?
##### import the library
```python
import greendeck_redis
```

##### import ```redis``` class
```python
from greendeck_redis import RedisQueue
from greendeck_redis import RedisSet
```

##### initialize ```redis``` client connection
```python
# declare variables
REDIS_HOST = <YOUR_REDIS_HOST>
REDIS_PORT = <YOUR_REDIS_PORT>
# Here default values are REDIS_PORT='', REDIS_HOST=''

redis_queue = RedisQueue(REDIS_HOST, REDIS_PORT, queue_name)
# OR/AND
redis_set = RedisSet(REDIS_HOST, REDIS_PORT, set_name)
```

---
How to build your pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5

# Thank You
