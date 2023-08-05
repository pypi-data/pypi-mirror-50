import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='bmetoolkit',  
     version='1',
     scripts=['mygui.py'] ,
     author="Patrick Chirdon",
     author_email="pc419714@ohio.edu",
     description="chemoinformatics toolkit",
     long_description=long_description,
   long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
