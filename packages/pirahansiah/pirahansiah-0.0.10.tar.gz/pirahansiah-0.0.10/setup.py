import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pirahansiah",
    version="0.0.10",
    author="Farshid PirahanSiah",
    author_email="pirahansiah@gmail.com",
    description="Farshid PirahanSiah workshop computer vision OpenCV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pirahansiah/farshid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

