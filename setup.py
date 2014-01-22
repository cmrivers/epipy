import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "epipy",
    version = "0.0.1",
    author = "Caitlin Rivers",
    author_email = "caitlinrivers@gmail.com",
    description = ("Python tools for epidemiology."),
    install_requires = ['Numpy >= 1.6.2',
                        'Matplotlib >=1.2.0',
                        'Networkx >=1.6.0',
                        'Pandas >= 0.12.0'],
    license = "MIT",
    keywords = "epidemiology",
    packages = ['epipy'],
    scripts = ['epipy/basics.py',
               'epipy/case_tree.py',
               'epipy/checkerboard.py',
               'epipy/data_generator.py',
                'epipy/epicurve.py'],
    #long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2.7",
        "Natural Language :: English",
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Medical Science Apps',],
)
