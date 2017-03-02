import os
import sys
import subprocess

# Fetch version from git tags, and write to version.py.
# Also, when git is not available (PyPi package), use stored version.py.
version_py = os.path.join(os.path.dirname(__file__), 'version.py')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    version_git = subprocess.check_output(
        ["git", "describe", "--tags"]).rstrip().decode("utf-8")
except:
    with open(version_py, 'r') as f:
        version_git = f.read().strip().split('=')[-1].replace('"', '')

version_msg = "# Do not edit this file. " \
              "# Pipeline versioning is governed by git tags."

with open(version_py, 'w') as f:
    f.write(version_msg + os.linesep + "__version__ = '{ver}'".format(
        ver=version_git) + '\n')

setup(name='InQRy',
      version="{ver}".format(ver=version_git),
      license='MIT',
      description='Gets machine specs and generates a QR code containing them',
      author='Eric Hanko',
      author_email='v-erhank@microsoft.com',
      packages=['inqry'],
      long_description=open('README.md').read(),
      install_requires=[
          "qrcode",
          "pyyaml",
          "pytest-runner",
          "pytest",
          "Pillow",
          "pypiwin32",
          "wmi"] + (["pypiwin32", "wmi"] if sys.platform == 'win32' else []),
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      )
