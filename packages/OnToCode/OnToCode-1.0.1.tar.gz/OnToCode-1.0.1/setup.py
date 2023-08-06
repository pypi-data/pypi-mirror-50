from contextlib import contextmanager
import subprocess
import operator
import os
import shutil
import sys

from distutils.cmd import Command
from pkg_resources import (add_activation_listener, normalize_path,
                           require, working_set)
from setuptools import setup


class BuildDocumentation(Command):
    """Run sphinx-apidoc and sphinx-build with project and dependencies on path

    This class was pieced together from `ptr.PyTest` of the pytest-runner
    library and its base class, `setuptools.command.test`.
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @contextmanager
    def _project_on_sys_path(self):

        self.run_command('egg_info')
        egg_info_command = self.get_finalized_command("egg_info")

        old_path = sys.path[:]
        old_modules = sys.modules.copy()

        try:
            project_path = normalize_path(egg_info_command.egg_base)
            sys.path.insert(0, project_path)
            working_set.__init__()
            add_activation_listener(lambda dist: dist.activate())
            require('%s==%s' % (egg_info_command.egg_name,
                                egg_info_command.egg_version))
            with self._paths_on_pythonpath([project_path]):
                yield
        finally:
            sys.path[:] = old_path
            sys.modules.clear()
            sys.modules.update(old_modules)
            working_set.__init__()

    @staticmethod
    @contextmanager
    def _paths_on_pythonpath(paths):
        nothing = object()
        orig_pythonpath = os.environ.get('PYTHONPATH', nothing)
        current_pythonpath = os.environ.get('PYTHONPATH', '')
        try:
            prefix = os.pathsep.join(paths)
            new_path = os.pathsep.join([prefix, current_pythonpath])
            if new_path:
                os.environ['PYTHONPATH'] = new_path
            yield
        finally:
            if orig_pythonpath is nothing:
                os.environ.pop('PYTHONPATH', None)
            else:
                os.environ['PYTHONPATH'] = orig_pythonpath

    def run(self):
        dist = self.distribution
        installed_dists = dist.fetch_build_eggs(dist.install_requires)
        paths = map(operator.attrgetter('location'), installed_dists)
        with self._paths_on_pythonpath(paths):
            with self._project_on_sys_path():
                subprocess.run(['sphinx-build', 'docs', 'build/sphinx/html'])


setup(
    name="OnToCode",
    version="1.0.1",
    license="LGPLv3+",
    url="https://gitlab.com/dlr-dw/ontocode",
    author="Philipp Matthias Schäfer",
    author_email="p.schaefer@dlr.de",
    classifiers= [
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    packages=["ontocode"],
    python_requires=">=3.6",
    install_requires=["Owlready2>=0.12", "rdflib>=4.2"],
    extras_require={'jinja2': ["Jinja2>=2.10"]},
    setup_requires=["pytest-runner", "pytest-pylint"],
    tests_require=["Jinja2>=2.10", "pylint-quotes", "pytest",
                   "pytest-codestyle", "pytest-cov", ],
    cmdclass={'docs': BuildDocumentation},
)
