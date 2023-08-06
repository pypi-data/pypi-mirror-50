import os
import sys
from setuptools import find_packages, setup

VERSION = "2.1.2"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()


setup(
    author="Luca Forzutti",
    author_email="luca@ahd-creative.com",
    description="semantic templates for artek apps",
    name="artek-templates",
    version=VERSION,
    url="http://github.com/AHDCreative/artek-templates/",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
        "django-bootstrap-form>=3.0.0"
    ],
    tests_require=[
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
