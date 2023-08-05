# Copyright 2018 The Rekcurd Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools.command.sdist import sdist
from setuptools import setup
import subprocess


here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'rekcurd_dashboard', '_project.py')).read())
exec(open(os.path.join(here, 'rekcurd_dashboard', '_version.py')).read())
PACKAGE_NAME = __project__  # NOQA
VERSION = __version__  # NOQA
DEVELOPMENT_STATUS = "3 - Alpha"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

EXTRAS = {}
REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        if ';' in line:
            requirement, _, specifier = line.partition(';')
            for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
            for_specifier.append(requirement)
        else:
            REQUIRES.append(line)

with open('test-requirements.txt') as f:
    TESTS_REQUIRES = f.readlines()

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


class rekcurd_dashboard_sdist(sdist):
    def run(self):
        subprocess.check_call('cd frontend && yarn install && yarn run build', shell=True)
        sdist.run(self)


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="A WebUI for managing machine learning services of Rekcurd.",
    long_description_content_type='text/markdown',
    author_email="",
    author="Rekcurd team and contributors",
    license="Apache License Version 2.0",
    url="https://github.com/rekcurd/dashboard",
    keywords=["Rekcurd", "Kubernetes", "Python", "gRPC", "Restful"],
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRES,
    extras_require=EXTRAS,
    packages=['rekcurd_dashboard', 'rekcurd_dashboard.apis',
              'rekcurd_dashboard.auth', 'rekcurd_dashboard.console_scripts',
              'rekcurd_dashboard.core', 'rekcurd_dashboard.data_servers',
              'rekcurd_dashboard.logger', 'rekcurd_dashboard.models',
              'rekcurd_dashboard.protobuf', 'rekcurd_dashboard.utils'],
    package_data={
        'rekcurd_dashboard': [
            'template/*',
            'static/**/*',
            'static/**/**/*'
        ],
    },
    include_package_data=True,
    long_description=LONG_DESCRIPTION,
    entry_points={
        'console_scripts': [
            'rekcurd_dashboard=rekcurd_dashboard.console_scripts:main',
        ],
    },
    cmdclass={
        'sdist': rekcurd_dashboard_sdist
    },
    classifiers=[
        "Development Status :: %s" % DEVELOPMENT_STATUS,
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
