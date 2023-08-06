from setuptools import setup, find_packages

NAME = 'sqlact'
DESCRIPTION="A python CLI client for composing SQL queries with content-based and history-aware auto-completion"
URL = 'https://github.com/ericmanzi/sqlact-cli'
EMAIL = 'manzieric424a@gmail.com'
AUTHOR = 'Eric Manzi',
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.3'

def requirements_file_to_list(fn="requirements.txt"):
  with open(fn, 'r') as f:
    return [x.rstrip() for x in list(f) if x and not x.startswith('#')]

def get_long_description(fn="README.md"):
  with open(fn, 'r') as f:
    return f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["test.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=[NAME],
    entry_points={
        'console_scripts': ['sqlact=sqlact.main:run'],
    },
    install_requires=requirements_file_to_list(),
    include_package_data=True,
    license='MIT',
)