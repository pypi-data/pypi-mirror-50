
"""A CI tool to deploy applications to Shipa instances
See:
https://github.com/shipa-corp/ci-integration
"""

from setuptools import setup, find_packages

description = 'A CI tool to deploy applications to Shipa instances'
url = 'https://github.com/shipa-corp/ci-integration'

setup(
    name='shipa-ci',
    version='0.0.7',
    description=description,
    long_description=
    description + '\n\n' + url,
    url=url,
    packages=find_packages(),
    py_modules=['shipa-ci', 'gitignore'],
    scripts=['shipa-ci.py'],
    install_requires=['requests>=2.22.0'],
    classifiers=[
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license='MIT',
    keywords='shipa-ci',
    platforms=['MacOS', 'Debian', 'Fedora', 'CentOS']
)
