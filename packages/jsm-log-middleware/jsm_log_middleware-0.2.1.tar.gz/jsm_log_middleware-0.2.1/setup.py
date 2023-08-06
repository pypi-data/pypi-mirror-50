import os

from setuptools import find_packages
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="jsm_log_middleware",
    version="0.2.1",
    description="Audit log",
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    author="Ricardo Baltazar Chaves",
    author_email="Ricardo Baltazar <ricardobchaves6@gmail.com>",
    license="MIT",
    url="https://github.com/juntossomosmais/castle-of-soure",
    packages=find_packages(exclude=["castle_of_soure.*", "castle_of_soure"]),
    install_requires=["request-id-django-log", "django-stomp", "jsm-user-services"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Environment :: Web Environment",
        "Natural Language :: Portuguese (Brazilian)",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
