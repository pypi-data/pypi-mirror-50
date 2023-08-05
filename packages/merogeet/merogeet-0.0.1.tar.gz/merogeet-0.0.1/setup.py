import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="merogeet",
    version="0.0.1",
    author="jungee",
    author_email="jungeebah@gmail.com",
    description="learning packaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jungeebah/merogeet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)