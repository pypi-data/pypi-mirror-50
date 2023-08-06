import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deep_learning",
    version="0.0.2",
    author="Bei Zhou",
    author_email="spencershuchen@gmail.com",
    description="Cover Mainstream Deep Learning Algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itengying/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)