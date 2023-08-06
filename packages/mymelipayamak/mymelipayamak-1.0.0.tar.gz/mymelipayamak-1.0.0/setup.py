from setuptools import setup, find_packages
import sys

requires = ['requests', 'zeep']

setup(
    name = "mymelipayamak",
    py_modules = ['mellipayamak'],
    version = "1.0.0",
    description = "MeliPayamak Python library",
    author = "Melipayamak Team",
    url = "https://github.com/Melipayamak/melipayamak-python",
    keywords = ["melipayamak", "sms"],
    packages=find_packages(),
    install_requires = requires,
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
        ]
     )