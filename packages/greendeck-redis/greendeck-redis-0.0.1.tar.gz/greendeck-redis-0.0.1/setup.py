import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="greendeck-redis",
    version="0.0.1",
    author="yashvardhan srivastava",
    author_email="yash@greendeck.com",
    description="Greendeck Redis Package",
    long_description="try it",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['greendeck_redis', 'greendeck_redis.src', 'greendeck_redis.src.redis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'redis', 'tqdm', 'json'
    ],
    include_package_data=True,
    zip_safe=False
)
