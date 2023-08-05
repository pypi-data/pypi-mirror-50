# setup.py
from setuptools import setup, find_packages
import pypandoc

long_description = pypandoc.convert('../README.md', 'rst')

setup(name='IronDomo',
      version='0.1.0',
      author='Matteo Ferrabone',
      author_email='matteo.ferrabone@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/desmoteo/IronDomo",
      packages=find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
      ],
      requires=['zmq']
      )

