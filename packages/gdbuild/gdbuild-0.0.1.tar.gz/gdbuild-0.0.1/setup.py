# Always prefer setuptools over distutils
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gdbuild',
    version='0.0.1',
    description='A python module used to help building Godot 3.1 games.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Chukobyte/GDBuild',
    author='Chukobyte',
    author_email='chukobyte@gmail.com',
    packages=['gdbuild'],
    python_requires='>=3.5',
    # install_requires=['none'],  # Optional
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Chukobyte/GDBuild/issues',
        'Source': 'https://github.com/Chukobyte/GDBuild',
    },
)
