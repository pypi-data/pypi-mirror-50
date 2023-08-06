import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywc",
    version="0.0.1",
    author="Ayush Jha",
    author_email="ayushjha@pm.me",
    description="A word counter with support for multiple languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ayys/pywc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
