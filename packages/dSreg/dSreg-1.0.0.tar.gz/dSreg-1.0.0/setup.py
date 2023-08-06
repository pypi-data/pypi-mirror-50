#!/usr/bin/env python

from setuptools import setup, find_packages
from dSreg.utils.settings import VERSION


def main():
    description='Joint inference of alternative splicing and regulatory changes'
    setup(
        name='dSreg',
        version=VERSION,
        description=description,
        author_email='cmarti@cnic.es',
        url='https://bitbucket.org/cmartiga/dSreg',
        packages=find_packages(),
        include_package_data=True,
        entry_points={
          'console_scripts': [
              'dSreg = bin.dsreg:main',
              'dsreg_plot = bin.dsreg_plot:main',
              'reg_enrichment = bin.reg_enrichment:main',
              'compile_models = bin.compile_models:main',
              ]}, 
        install_requires=['pandas == 0.25.0',
                          'scipy == 1.3.0',
                          'matplotlib == 3.1.0',
                          'seaborn == 0.9.0',
                          'statsmodels == 0.10.1',
                          'pystan == 2.18.0.0',
                          ][::-1],
        platforms = 'ALL',
        keywords = ['bioinformatics', 'Splicing regulation',
                    'alternative splicing', 'RNA-Seq',
                    'probabilistic models', 'bayesian'],
        classifiers=[
            "Programming Language :: Python :: 3",
            'Intended Audience :: Science/Research',
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
         )
    return

if __name__ == '__main__':
    main()
