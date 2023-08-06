
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='flask_ordering',  
     version='0.0.2',
     author="Sandakin Gunadasa",
     author_email="sandakinh@gmail.com",
     description="flask-rest-api reponse ordering",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url=" ",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )