import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='my-1',  
     version='50',
     author="MOHD BILAL AZIZ",
     author_email="bilal.aziz9680@gmail.com",
     description="HELLO FUNCTION",
     long_description=long_description,
     url="",
     packages=setuptools.find_packages(),
     classifiers=(
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ),
 )
