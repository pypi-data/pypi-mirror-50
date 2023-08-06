import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ucam-managed-mac-utils",
    version="0.0.3",
    author="James Nairn",
    author_email="jwrn3@cam.ac.uk",
    description="A collection of useful functions for managing Macs at University of Cambridge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.developers.cam.ac.uk/uis/desktopsystems/ucam_managed_mac_utils.git',
    install_requires=['pyobjc'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
