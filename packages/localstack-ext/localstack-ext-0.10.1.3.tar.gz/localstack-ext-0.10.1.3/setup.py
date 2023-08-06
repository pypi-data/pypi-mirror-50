#!/usr/bin/env python

import os
import re
import subprocess
from setuptools import find_packages, setup
from setuptools.command.install import install
try:
    from urllib2 import urlopen  # Python 2
except Exception:
    from urllib.request import urlopen  # Python 3

install_requires = []
dependency_links = []

# root code folder
THIS_FOLDER = os.path.realpath(os.path.dirname(__file__))

# See https://github.com/dashingsoft/pyarmor/issues/53
PYTRANSFORM_MUSL_URL = 'http://pyarmor.dashingsoft.com/downloads/platforms/alpine/_pytransform.so'


def run(cmd):
    return subprocess.check_output(cmd, shell=True)


def is_alpine():
    try:
        run('cat /etc/issue | grep Alpine > /dev/null')
        return True
    except Exception:
        return False


def download(url, target):
    response = urlopen(url)
    data = response.read()
    with open(target, 'wb') as out_file:
        out_file.write(data)


# determine version
with open(os.path.join(THIS_FOLDER, 'localstack_ext', 'constants.py')) as f:
    configs = f.read()
version = re.search(r'^\s*VERSION\s*=\s*[\'"](.+)[\'"]\s*$', configs, re.MULTILINE).group(1)

# read requirements
with open(os.path.join(THIS_FOLDER, 'requirements.txt')) as f:
    requirements = f.read()

for line in re.split('\n', requirements):
    if line and line[0] == '#' and '#egg=' in line:
        line = re.search(r'#\s*(.*)', line).group(1)
    if line and line[0] != '#':
        if '://' not in line:
            install_requires.append(line)


# define post-install commands
class PostInstallCommand(install):
    def run(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)
        print('is_alpine()', is_alpine())
        if is_alpine():
            # Fetch libmusl compatible version of _pytransform.so
            target_file = 'localstack_ext/_pytransform.so'
            print('downloading %s to %s' % (PYTRANSFORM_MUSL_URL, target_file))
            print(run('ls -la'))
            print(run('pwd'))
            print(run('ls -la %s || true' % target_file))
            download(PYTRANSFORM_MUSL_URL, target_file)


package_data = {
    '': ['*.md'],
    'localstack_ext': [
        '_pytransform*',
        'license.lic',
        'pytransform.key',
        'utils/*.py.enc',
        'utils/aws/*.py.enc',
        'services/*.py.enc',
        'services/apigateway/*.py.enc',
        'services/awslambda/*.py.enc',
        'services/cognito/*.py.enc',
        'services/ec2/*.py.enc',
        'services/iam/*.py.enc',
        'services/sqs/*.py.enc',
        'services/sts/*.py.enc'
    ]}


if __name__ == '__main__':

    setup(
        name='localstack-ext',
        version=version,
        description='Extensions for LocalStack',
        author='Waldemar Hummer',
        author_email='waldemar.hummer@gmail.com',
        url='https://github.com/localstack/localstack',
        packages=find_packages(exclude=('tests', 'tests.*')),
        package_data=package_data,
        install_requires=install_requires,
        dependency_links=dependency_links,
        cmdclass={
            'install': PostInstallCommand
        },
        test_suite='tests',
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Testing',
        ]
    )
