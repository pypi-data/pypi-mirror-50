import sys
from setuptools import setup

# This check and everything above must remain compatible with Python 2.7.
if sys.version_info[:2] < (3, 6):
    raise SystemExit("Python >= 3.6 required.")

import benc  # noqa

setup(
    name='benc',
    version=benc.__version__,
    description='Bencoder for the modern world',
    long_description=(
        'Bencoder in 100 lines of modern Python (MIT License).'
    ),
    url='https://github.com/notpeter/benc',
    author='Peter Tripp',
    author_email='notpeter@notpeter.net',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='benc bencode',
    packages=['benc'],
    python_requires='>=3.6',
    install_requires=[],
)
