from setuptools import setup
from setuptools import find_packages
import os


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), "rb") as f:
    long_description = f.read().decode("utf-8")


def get_version():
    with open(os.path.join("rexart", "__init__.py"), "r") as f:
        for line in f.readlines():
            if "__version__ = " in line:
                return line.strip().split(" = ")[-1][1:-1]


setup(
    name="rexart",
    version=get_version(),
    scripts=[],
    url="https://github.com/douglasdavis/rexart",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": ["rexart = rexart._app:cli"]},
    description="Make some art out of TRExFitter output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Doug Davis",
    author_email="ddavis@ddavis.io",
    license="BSD 3-clause",
    test_suite="tests",
    python_requires=">=3.7",
    install_requires=requirements,
    tests_require=["pytest>=4.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
