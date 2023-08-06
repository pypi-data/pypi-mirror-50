import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()
setuptools.setup(
    name="biotensor",
    version="0.0.1",
    author_email="qq525399365@gmail.com",
    description="no description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ], 
)
