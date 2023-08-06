from setuptools import setup, find_packages

setup(
    name="package_one",
    packages=find_packages(),
    version="0.1",
    description="First package created and uploaded to pypi",
    author="Bharath Yadavally",
    author_email="bharath.yadavally@gmail.com",
    url="https://github.com/bh4r4th/python_package_one",
    download_url="https://github.com/bh4r4th/python_package_one/tarball/0.1",
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
