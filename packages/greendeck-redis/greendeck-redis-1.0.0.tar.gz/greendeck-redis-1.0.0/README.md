greendeck-redis
---
**Created for internal ```Greendeck``` use only. Can be used for non-commercial purposes.**

![Greendeck][gd]  ![redis][redis]

[gd]: https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/gd_transparent_blue_bg.png "Logo Title Text 2"
[redis]: https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/redis.png "Logo Title Text 2"

A simple Redis library to create Redis sets and Redis queues and perform basic operations on them.

### Install from pip
https://pypi.org/project/greendeck-redis/

```pip install greendeck-redis```

### How to use ?
##### import the library
```python
import greendeck_redis
```

##### or, import ```redis``` classes
```python
from greendeck_redis import RedisQueue
from greendeck_redis import RedisSet
from greendeck_redis import Redis # This will be used for operations that require two or more redis keys (Set or Queue)
```

##### initialize ```redis``` client connection as per your requirements
```python
# declare variables
REDIS_HOST = <YOUR_REDIS_HOST>
REDIS_PORT = <YOUR_REDIS_PORT>
REDIS_PASSWORD = <YOUR_REDIS_PASSWORD>
# Here default values are REDIS_PORT='', REDIS_HOST='', REDIS_PASSWORD=None

redis_queue = RedisQueue(REDIS_HOST, REDIS_PORT, queue_name, password=REDIS_PASSWORD)
# OR/AND
redis_set = RedisSet(REDIS_HOST, REDIS_PORT, set_name, password=REDIS_PASSWORD)
# OR/AND
redis_client = Redis(REDIS_HOST, REDIS_PORT, password=REDIS_PASSWORD) # This will be used for operations that require two or more redis keys (Set or Queue)
```

##### using ```redis set```
```python
redis_set.smembers() # will return all the member strings of the RedisSet ```redis_set``` in a python list.
redis_set.scard() # will return the count of members of the RedisSet ```redis_set``` as an integer.
redis_set.put(item) # will insert ```item``` string in the RedisSet ```redis_set``` if not already present. RedisSet doesn't allow dupicate values.
```

##### using ```redis``` for finding difference of two redis sets
```python
redis_client.sdiffstore(target_set_name, operand1_set_name, operand2_set_name) # this creates a new RedisSet with the name ```target_set_name``` and contains the difference of ```operand1_set_name``` and ```operand2_set_name```.
```

##### using ```redis queue```
```python
redis_queue.qsize() # will return the count of members of the RedisQueue ```redis_queue``` as an integer.
redis_queue.put(item) # will insert ```item``` string in the RedisQueue ```redis_queue``` even if it is already present. RedisQueue allows duplicate values.
redis_queue.empty() # will clear all the member strings of the RedisQueue ```redis_queue``` in a python list.
redis_queue.get() # will return the first member string (single) of the RedisQueue ```redis_queue``` as a string.
redis_queue.get_multi(n) # will return the first ```n``` member strings (count: n) of the RedisQueue ```redis_queue``` as a python list. if the count of members in the RedisQueue is less than ```n```; it will return all the members as a python list.
redis_queue.get_nowait() # will return all members of the RedisQueue ```redis_queue``` as a python list.

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
