from setuptools import setup

setup(
    name="varlink",
    packages=["varlink"],
    version = "30.3.0",
    description="Varlink",
    long_description="Python implementation of the varlink protocol http://varlink.org",
    author="Lars Karlitski<lars@karlitski.net>, Harald Hoyer<harald@redhat.com>",
    author_email="harald@redhat.com",
    url="https://github.com/varlink/python",
    license="ASL 2.0",
    keywords="ipc varlink rpc",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    package_data={
        "varlink": ["*.varlink"]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: System :: Networking"
    ]
)
