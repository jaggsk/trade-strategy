from setuptools import setup
import os
import re

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

version = get_version('trade_strat')

for i in required:
    print(str(i))
#print(required)

setup(
    name='trade-strategy',
    version=version,
    packages=['trade_strat',
              'trade_strat.indicators',
              'trade_strat.signals',
              'trade_strat.strategies'],
    description='Python package to apply trading algorithms to financial instruments',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url= "https://github.com/jaggsk/trade-strategy",
    author='Kevin Jaggs',
    license='MIT',
    author_email='kevin.jaggs@gmail.com',
    install_requires=[required],
    #keywords='python git setup example',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)