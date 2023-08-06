import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyGreatCircleDistance",
    version="0.0.1",
    author="Aleksandr Shpak",
    author_email="shpaker@gmail.com",
    description="Calculate the distance between two GPS coordinates in meters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shpaker/pyGreatCircleDistance",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
