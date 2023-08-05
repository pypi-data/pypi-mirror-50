import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='evergreen_p_convolution',  
     version='1.0.1',
     author="Rice",
     author_email="mrseanrice@gmail.com",
     description="A python p_convolve package based on evergreenforest",
     long_description=long_description,
   long_description_content_type="text/markdown",
     packages =setuptools.find_packages(),
     include_package_data=True,
     classifiers=[
         "Programming Language :: Python :: 2.7",
         "License :: OSI Approved :: MIT License",
     ],
 )
