import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="name-generator",
    version="0.1",
    author="Rapciu",
    author_email="mrapczewski711@gmail.com",
    description="Generates a random name/username.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rapciu/name-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
)
