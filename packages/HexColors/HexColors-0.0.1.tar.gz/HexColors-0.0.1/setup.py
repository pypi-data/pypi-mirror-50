import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HexColors",
    version="0.0.1",
    author="Reggles",
    author_email="reginaldbeakes@gmail.com",
    description="Organized Hex Color Tuples",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Reggles44/hex-colors",
    packages=['hexcolors'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)