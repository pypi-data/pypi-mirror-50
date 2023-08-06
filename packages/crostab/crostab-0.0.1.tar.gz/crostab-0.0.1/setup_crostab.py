import setuptools

__name__ = 'crostab'
__version__ = '0.0.1'
__root__ = 'src'
__keywords__ = ["cross-table", "analytics", "pivot"]
__description__ = "A simple cross-table analysis tool"


def including(kw):
    return f"*.{kw}", f"*.{kw}.*", f"{kw}.*", f"{kw}"


def read_install_requires():
    reqs = [
        'xbrief>=0.0.1',
        'veho>=0.0.1',
        'borel>=0.0.1',
    ]
    return reqs


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__name__,
    version=__version__,
    author="Hoyeung Wong",
    author_email="hoyeungw@outlook.com",
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoyeungw/",
    install_requires=read_install_requires(),
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
