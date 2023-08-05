from setuptools import setup
import re

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('folders2json/folders2json.py').read(),
    re.M
).group(1)

setup(
    name='folders2json',
    author='James Campbell',
    author_email='jc@normail.co',
    version=version,
    license='GPL',
    description='file extension info',
    packages=['folders2json'],
    py_modules=['folders2json', 'functions'],
    keywords=['folders', 'json',
              'files', 'directories', 'data-structuring'],
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    include_package_data=True,
    install_requires=[
        'argparse',
        'pathlib'
    ],
    entry_points={
        'console_scripts': [
            'folders2json=folders2json.folders2json:main',
        ],
    },
    url='https://github.com/jamesacampbell/folders2json',
    download_url=f'https://github.com/\
        jamesacampbell/folders2json/archive/{version}.tar.gz'
)
