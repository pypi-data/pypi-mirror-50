import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='paramctl',  
     version='0.056',
     author="Angel Alonso",
     author_email="alonsofonseca.angel@gmail.com",
      description='Manage nested parameters through a json file',
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/angelalonso/pctl",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
     ],
     python_requires='>=3',
 )
