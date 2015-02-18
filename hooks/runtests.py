"""
Runs the tests.

This scripts is to be executed from the root of the Git repository.
"""

from __future__ import print_function

import os
import sys
import subprocess
import itertools
import yaml


VIRTUALENV_PREFIX = '.chromalog'


def get_virtualenv_python(python_version):
    virtualenv_path = '{prefix}{version}'.format(
        prefix=VIRTUALENV_PREFIX,
        version=python_version,
    )

    if os.path.isdir(virtualenv_path):
        if sys.platform == 'win32':
            return virtualenv_path, os.path.join(virtualenv_path, 'Scripts')
        else:
            return virtualenv_path, os.path.join(virtualenv_path, 'bin')

    return None, None


def main():
    travis_configuration = next(yaml.load_all(open('.travis.yml')))

    for python_version in travis_configuration.get('python'):
        virtualenv_path, bin_path = get_virtualenv_python(python_version)

        if not virtualenv_path or not bin_path:
            print("No virtualenv found for python {}.".format(python_version))
        else:
            print("Running tests for python {}...".format(python_version))

            environment = os.environ.copy()
            environment['PATH'] = os.pathsep.join([
                bin_path,
                environment.get('PATH', ''),
            ])

            try:
                for command in itertools.chain(
                        travis_configuration.get('install', []),
                        travis_configuration.get('script', []),
                ):
                    print(command)
                    subprocess.check_call(
                        command,
                        shell=True,
                        env=environment,
                    )
            except subprocess.CalledProcessError as ex:
                print(
                    (
                        "Failure when running tests for python {}. Command"
                        " returned exit status {}."
                    ).format(
                        python_version,
                        ex.returncode,
                    )
                )
            else:
                print("Done running tests for python {}.".format(python_version))


if __name__ == '__main__':
    main()
