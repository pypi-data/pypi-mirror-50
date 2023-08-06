import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='nanimsave',  
     version='0.1',
     author="Sebastien Drouyer",
     author_email="sdrdis@gmail.com",
     description="Save images that contain nan values",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/sdrdis/nanimsave",
     packages=['nanimsave'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )