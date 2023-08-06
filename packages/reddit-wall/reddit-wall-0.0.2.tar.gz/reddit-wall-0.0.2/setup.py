import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reddit-wall",
    version="0.0.2",
    author="Jalen Adams",
    author_email="jalen@jalenkadams.me",
    description="Download wallpapers from subreddits and multireddits of your choosing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeftySolara/reddit-wall",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Natural Language :: English"
    ],
)
