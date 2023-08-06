import setuptools
with open("README.md","r") as fh:
    long_description=fh.read()
setuptools.setup(
    name="bjj",
    version="0.0.1",
    author_email="525399365@qq.com",
    description="wu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ], 
)
