import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pirahansiah",
    version="0.0.4",
    author="Farshid PirahanSiah",
    author_email="pirahansiah@gmail.com",
    description="farshid pirahansiah workshop computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pirahansiah/pirahansiah",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

