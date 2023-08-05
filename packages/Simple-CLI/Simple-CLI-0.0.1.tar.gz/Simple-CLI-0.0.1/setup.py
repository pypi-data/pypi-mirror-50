import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Simple-CLI",
    version="0.0.1",
    author="Alex Manning",
    author_email="alex.manning9904@gmail.com",
    description="Python CLI Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexmanning9904/simple-cli/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)