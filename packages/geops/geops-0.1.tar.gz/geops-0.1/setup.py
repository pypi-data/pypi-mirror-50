from setuptools import setup, find_packages
from geops import __version__

with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name="geops",
    version=__version__,
    author="Tokarev Artem",
    author_email="tokarev28.art@gmail.com",
    packages=find_packages(),
    description="Python frontend for Gmsh scripting language.",
    # long_description=readme,
    license="MIT",
    platforms="any",
    install_requires=["numpy >= 1.9"],
    python_requires=">=3",
    keywords=["mesh", "gmsh", "mesh generation", "mathematics"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
