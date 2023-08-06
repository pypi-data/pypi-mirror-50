import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
       name          ='frankyuan',
       version       ='1.1.0',
       py_modules    =['frankyuan'], 
       author        ='Fuyvlanling',
       author_email  ='1946001033@qq.com',
       url           ='http://www.headfirstlabs.com',
       description   ='A simple printer of nested lists',
       long_description=long_description,
       packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
       )
