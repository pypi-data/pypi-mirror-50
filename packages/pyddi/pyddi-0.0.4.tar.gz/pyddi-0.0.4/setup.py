import os
from setuptools import setup, find_packages

pkg = 'pyddi'
__version__ = "0.0.4"
build_root = os.path.dirname(__file__)

scripts = ["bin/" + j for j in os.listdir("bin") ]

requires = [
    "numpy",
    "astropy",
    "argparse",
    "astro-tigger"
]

def readme():
    """Get readme content for package long description"""
    with open(os.path.join(build_root, 'README.md')) as f:
        return f.read()


setup(name = pkg,
    version=__version__,
    description="Identifies Sources that Require Direction-Dependent Calibration.",
    author="Lerato Sebokolodi",
    author_email="mll.sebokolodi@gmail.com",
    url="https://github.com/Sebokolodi/pyddi",
    long_description=readme(),
    long_description_content_type = 'text/markdown',
    packages=find_packages(),
    install_requires=requires,
    scripts=scripts,
    include_package_data=True,
    license="GNU GPL v3",
    classifiers=["Intended Audience :: Developers",
                 "Topic :: Scientific/Engineering :: Astronomy",
                 "Topic :: Software Development :: Libraries :: Python Modules"])

