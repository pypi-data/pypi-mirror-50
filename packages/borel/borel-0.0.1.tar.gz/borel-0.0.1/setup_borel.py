import setuptools

__root__ = 'src'
__keywords__ = ["math", "statistics", "calculate"]
__name__ = 'borel'


def including(kw):
    return f"*.{kw}", f"*.{kw}.*", f"{kw}.*", f"{kw}"


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__name__,
    version="0.0.1",
    author="Hoyeung Wong",
    author_email="hoyeungw@outlook.com",
    description="A math tool-box",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoyeungw/",
    package_dir={'': __root__},
    packages=setuptools.find_packages(where=__root__,
                                      include=including(__name__)),
    keywords=__keywords__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
