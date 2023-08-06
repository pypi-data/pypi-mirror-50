from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="package_one",
    packages=find_packages(),
    version="0.3",
    description="First package created and uploaded to pypi",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Bharath Yadavally",
    author_email="bharath.yadavally@gmail.com",
    url="https://github.com/bh4r4th/python_package_one",
    download_url="https://github.com/bh4r4th/python_package_one/tarball/0.3",
    keywords=['bh4r4th', 'pypi', 'package'],  # arbitrary keywords,
    install_requires=[
        'pytest==5.0.1'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts':[
            'hello_world = package_one.hello_world.print_hello_world'
        ]
    },
)
