#!/usr/bin/env python

from argparse import ArgumentParser, RawTextHelpFormatter
from collections import namedtuple
import os
import re
import subprocess
import shutil
import sys
import glob

import dsvenv.__main__ as dsvenv


# path to the directories
_VENV_NAME = '.venv'


##################################################

# This script can only be executed from a suitable virtual environment, i.e., the executable is located at
# `<_venv_name>/Scripts/python.exe`. Assuming that the virtual environment is always created at the top-level
# of a logical project or package, this allows for a robust way of determining this top-level/main dir.
VENV_DIR = os.path.realpath(os.path.join(os.path.dirname(sys.executable), '..'))

if not os.path.basename(VENV_DIR) == _VENV_NAME:
    raise RuntimeError('The `dsbuild` package can only be run from a virtual environment.')


def get_main_dir():
    """
    Get the top-level/main directory for this project or package.

    Returns:
        str: A path to the main directory.
    """
    return os.path.realpath(os.path.join(VENV_DIR, '..'))


def get_venv_dir():
    """
    Get the full path to the directory that is supposed to contain the local virtual environment.
    """
    return VENV_DIR


def get_venv_executable(executable):
    """ See dsvenv.get_venv_executable. """
    return dsvenv.get_venv_executable(get_venv_dir(), executable)


def get_venv_python():
    """ See dsvenv.get_venv_executable. """
    return dsvenv.get_venv_python(get_venv_dir())


##################################################
# Helpers to define the modes of this script.

modes = dict()

ModeFunction = namedtuple('ModeFunction', 'func description')

def register(description):
    def decorator_register(func):
        global modes
        function_prefix = 'mode_'
        assert func.__name__.startswith(function_prefix), \
                f'Function name of a mode should start with a literal \'{function_prefix}\'.'
        modes[func.__name__[len(function_prefix):]] = ModeFunction(func, description)
        return func

    return decorator_register


def get_valid_modes():
    return list(modes.keys())


def format_mode_description():
    max_len = len(max(get_valid_modes(), key=len))

    result = []
    for k, v in modes.items():
        result.append('{0:>{max_len}}: {1}'.format(k, v.description, max_len=max_len))

    return '\n'.join(result)


##################################################

def get_is_devops_build():
    """
    Check if the build is an Azure Devops build.
    This is done by checking if the BUILD_REQUESTEDFOR environment variable exists.

    Returns:
        bool: True if Azure Devops build, False if development build
    """
    return 'BUILD_REQUESTEDFOR' in os.environ


def get_git_version():
    """
    Get the current commit id and check if the repo is clean or dirty.

    Returns:
        (str, bool): the short git commit id and a bool indicating whether your local work directory is clean
    """
    main_dir = get_main_dir()
    try:
        r = subprocess.run(['git', 'describe', '--always', '--dirty', '--match', ';notag;'],
                           cwd=main_dir, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           universal_newlines=True)
        out = r.stdout.strip()
        git_version = out.split('-')
        if len(git_version) == 1:
            commit_id, is_dirty = (git_version[0], False)
        elif len(git_version) == 2:
            commit_id, is_dirty = (git_version[0], True)
        else:
            raise ValueError('Invalid git describe version: %s' % out)
    except subprocess.CalledProcessError:
        commit_id = 'unknown'
        is_dirty = False

    return commit_id, is_dirty


def get_version_from_changelog(changelog_path=None):
    """
    Get the version from the [Unreleased:d.d.d] title in the changelog.

    Args:
        changelog_path (str or None): Path to the changelog, if None, Changelog.md relative to this python file is used.

    Returns:
        (str, str, str): The major, minor and bugfix version found in the changelog

    Raises:
        ValueError: When no version was found in the changelog
    """
    main_dir = get_main_dir()
    if changelog_path is None:
        changelog_path = os.path.join(main_dir, 'Changelog.md')

    with open(changelog_path, 'rt') as fid:
        text = fid.read()

    unreleased_match = re.findall('##\s*\[\s*Unreleased\s*:\s*(\d+).(\d+).(\d+)\s*\]', text, flags=re.IGNORECASE)
    try:
        return unreleased_match[0][0], unreleased_match[0][1], unreleased_match[0][2]
    except IndexError:
        raise ValueError('No unreleased version match was found in Changelog.md, correct the changelog.')


def get_version_info(changelog_path=None):
    """
    Get the version info.
    The main_version is based on the version from the [Unreleased:d.d.d] title in the changelog.
    The post_version is only used for non-devops builds and based on git describe (commit id + dirty).
    The is_devops_build indicates if the build is an Azure Devops build.

    Args:
        changelog_path (str or None): Path to the changelog, if None, Changelog.md relative to this python file is used.

    Returns:
        (str, str or None, bool): The main_version, the post_version and the is_devops_build bool
    """
    version = get_version_from_changelog(changelog_path=changelog_path)
    is_devops_build = get_is_devops_build()
    main_version = '.'.join(version)

    if is_devops_build:
        post_version = None
    else:
        commit_id, is_dirty = get_git_version()
        post_version = ['dev', commit_id]
        if is_dirty:
            post_version += ['dirty']
        post_version = '.'.join(post_version)

    return main_version, post_version, is_devops_build


def get_version(changelog_path=None):
    """
    Get the complete version string.
    If the build is an Azure Devops build, the version does not have a post version: 0.0.1
    If the build is a local development build, the version will have a main and post version: 0.0.1+dev.a8452ass.dirty

    Args:
        changelog_path (str or None): Path to the changelog, if None, Changelog.md relative to this python file is used.

    Returns:
        str: The version string
    """
    main_version, post_version, _ = get_version_info(changelog_path=changelog_path)
    if post_version is not None:
        return main_version + '+' + post_version
    else:
        return main_version

##################################################

def find_library(folder):
    """
    Find the python library in a folder and check if it is a normal library or part of a namespace package.

    Args:
        folder (str): the folder containing the setup.py file

    Returns:
        str, bool: path to library, False if normal library, True if namespace package
    """
    from setuptools import find_packages
    from setuptools import find_namespace_packages
    try:
        package = find_packages(folder, exclude='*.*')[0]
        is_namespace_pkg = False
    except IndexError:
        pass
    try:
        package = find_namespace_packages(folder)
        package = [p for p in package if '.' not in p]
        package = package[0]
        is_namespace_pkg = True
    except IndexError:
        raise FileNotFoundError('No library could be found in:', folder)
    return os.path.join(folder, package), is_namespace_pkg


def get_libraries():
    """
    Get the paths to the python library-containing folders present in the directory of this script.
    Libraries can either be found by `find_packages('.')` or by searching for `setup.py` files in the `./lib` folder.

    Returns:
        list of str: a list of folders that contain the python library (the folder containing the setup.py file)
    """
    from setuptools import find_packages
    main_dir = get_main_dir()
    try:
        _ = find_packages(main_dir, exclude=('*.*',))[0]
        return [main_dir]
    except IndexError:
        pass

    setup_files = glob.glob(os.path.join(main_dir, 'lib', '**', 'setup.py'), recursive=True)
    if len(setup_files) == 0:
        raise ValueError(f'No python libraries could be found in {main_dir}')

    return [os.path.dirname(f) for f in setup_files]


##################################################
# Mode definition

@register(description='Print help.')
def mode_help():
    subprocess.check_call([sys.executable, __file__, '--help'])


@register(description='Clean wheel and docs folder to ensure a clean build.')
def mode_clean():
    """
    Clean the wheel and docs folder to ensure a clean build.
    """
    dirs_to_clean = ['wheel', 'docs/build']

    main_dir = get_main_dir()
    for dirname in dirs_to_clean:
        path = os.path.abspath(os.path.join(main_dir, dirname))
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
        except (PermissionError, OSError):
            raise OSError(f'The folder {path} could not be deleted, '
                           'so we are not sure that all build files are fresh.')
        print(f'Cleaned directory \'{path}\'.')


@register(description='Build documentation.')
def mode_docs():
    """
    Build the documentation.
    """
    lib_version = get_version()
    main_dir = get_main_dir()

    docs_dir = os.path.join(os.path.join(main_dir, 'docs'))
    if not os.path.exists(docs_dir):
        print(f'Directory \'{docs_dir}\' does not exist. No documentation will be generated.')
        return

    build_dir = os.path.join(docs_dir, 'build')
    html_dir = os.path.join(build_dir, 'html')
    source_dir = os.path.join(docs_dir, 'source')

    # python and sphinx-apidoc executable
    vpython = get_venv_python()
    sphinx_apidoc = get_venv_executable(executable='sphinx-apidoc.exe')

    # run sphinx-apidoc
    libs = get_libraries()
    for lib_dir in libs:
        # @Peter: The following call imposes the requirement `setuptools>41.0.0` on the _system_ Python, no??
        lib_folder, is_namespace_pkg = find_library(lib_dir)

        command = [sphinx_apidoc, '-o', source_dir, lib_folder, '-f', '-e']
        if is_namespace_pkg:
            command += ['--implicit-namespaces']

        subprocess.check_call(command, cwd=main_dir)

    # run sphinx
    command = [vpython, '-m', 'sphinx', source_dir, html_dir]
    subprocess.check_call(command, cwd=main_dir)

    # Copy and version docs
    wheel_dir = os.path.abspath(os.path.join(main_dir, 'wheel'))
    wheel_docs = os.path.join(wheel_dir, f'docs_{lib_version}')
    # TODO: The following will fail if `wheel_docs` already exists.
    shutil.copytree(src=html_dir, dst=wheel_docs)
    print('Docs copied to:', wheel_docs)

    # Copy Changelog.md
    changelog_src = os.path.join(main_dir, 'Changelog.md')
    changelog_dst = os.path.join(wheel_dir, f'Changelog_{lib_version}.md')
    shutil.copyfile(src=changelog_src, dst=changelog_dst)
    print('Changelog copied to:', changelog_dst)


@register(description='Build wheel.')
def mode_wheel():
    """
    Build a wheel of the library.
    """
    main_dir = get_main_dir()
    wheel_dir = os.path.abspath(os.path.join(main_dir, 'wheel'))

    libraries = get_libraries()
    for library in libraries:
        lib_name = os.path.basename(library)
        build_dir = os.path.join(wheel_dir, f'build-{lib_name}')
        bdist_dir = os.path.join(wheel_dir, f'bdist-{lib_name}')

        # run the wheel creation command
        command = [get_venv_python(), 'setup.py', 'build', '-b', build_dir, 'bdist_wheel',
                   f'--bdist-dir={bdist_dir}', f'--dist-dir={wheel_dir}', '-k']
        subprocess.check_call(command, cwd=library)

    print(f'Wheel created in \'{wheel_dir}\'')


@register(description='Run unittests + coverage.')
def mode_test():
    """
    Run unittests and coverage report. The tests are being picked up from a directory with name matching the
    pattern `*_test`. Note that at most a single directory on disk should match. If not, this is considered a
    fatal error.
    """
    main_dir = get_main_dir()

    # check if we can find libraries, otherwise raise exception
    _ = get_libraries()

    # find *_test folders
    test_folders = [f for f in glob.glob(os.path.join(main_dir, '*_test')) if os.path.isdir(f)]

    if len(test_folders) == 0:
        print(f'Could not find a `*_test` folder with unittests. No tests will be run.')
        return

    if len(test_folders) > 1:
        raise FileNotFoundError(f'Could not find a unique `*_test` folder with unittests. Found: '
                                f'{test_folder}.')

    test_folder = os.path.basename(test_folders[0])
    lib_name = test_folder.replace('_test', '')

    # run tests
    command = [get_venv_python(), '-m', 'pytest', test_folder,
                f'--junitxml={test_folder}_results/test-results.xml',
                f'--cov={lib_name}', f'--cov-report=xml:{test_folder}_results/coverage.xml',
                f'--cov-report=html:{test_folder}_results/html']
    subprocess.check_call(command, cwd=main_dir)

    print('Ran all unittests.')


@register(description='Print the library version.')
def mode_version():
    """
    Print library version.
    """
    lib_version = get_version()
    print(lib_version)


@register(description='Create/update local virtual environment.')
def mode_venv():
    """
    Create a local virtual environment using the requirements.txt file.
    """
    reqs_file = os.path.join(get_main_dir(), 'requirements.txt')

    # Change of working dir to the directory containing the requirements file!
    os.chdir(os.path.dirname(reqs_file))

    # Replace(!) the currently running process with the `pip install` call.
    vpython = get_venv_python()
    os.execv(vpython, [vpython, '-m', 'dsvenv', get_venv_dir(), '-r', reqs_file])


@register(description='clean + test + docs + wheel.')
def mode_all():
    """
    Convenience mode that does 'everything' from scratch (build, test, packaging).
    """
    mode_clean()
    mode_test()
    mode_docs()
    mode_wheel()


@register(description='clean + docs + wheel.')
def mode_package():
    """
    Convenience mode that does a clean packaging.
    """
    mode_clean()
    mode_docs()
    mode_wheel()


##################################################

def main():
    parser = ArgumentParser(prog='dsbuild',
                            formatter_class=RawTextHelpFormatter,
                            description='This script helps to build and package python libraries.\n' +
                                            format_mode_description())

    parser.add_argument('mode', default='all', const='all', nargs='?', choices=get_valid_modes())
    args = parser.parse_args()

    try:
        modes[args.mode].func()
    except KeyError as e:
        raise ValueError(f'Bad input mode \'{args.mode}\'.')


if __name__ == '__main__':
    main()
