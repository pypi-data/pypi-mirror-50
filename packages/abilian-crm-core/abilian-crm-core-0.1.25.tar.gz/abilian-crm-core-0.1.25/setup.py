# coding=utf-8
from __future__ import absolute_import, print_function, unicode_literals

from distutils.command.build import build as _build

import setuptools
from setuptools.command.develop import develop as _develop
from setuptools.command.sdist import sdist as _sdist

requirements = [l.strip() for l in open("requirements.in") if l.strip()]


class build(_build):
    sub_commands = [("compile_catalog", None)] + _build.sub_commands


class sdist(_sdist):
    sub_commands = [("compile_catalog", None)] + _sdist.sub_commands


class develop(_develop):
    def run(self):
        _develop.run(self)
        self.run_command("compile_catalog")


setuptools.setup(
    name="abilian-crm-core",
    use_scm_version=True,
    url="https://github.com/abilian/abilian-crm-core",
    license="LGPL",
    author="Abilian SAS",
    author_email="contact@abilian.com",
    description="Core framework for CRM applications",
    packages=["abilian.crm"],
    zip_safe=False,
    platforms="any",
    setup_requires=["babel", "setuptools-git", "setuptools_scm"],
    install_requires=requirements,
    extras_require={},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Flask",
    ],
    cmdclass={"build": build, "sdist": sdist, "develop": develop},
)
