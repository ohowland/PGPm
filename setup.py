import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="PGPm",
    version="0.0.1",
    author="Owen Edgerton",
    author_email="owen@howlandedgerton.com",
    description="PowerWind Alarm Monitor",
    long_description=long_description,
    url="https://github.com/ohowland/pgpm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Lanauge :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)