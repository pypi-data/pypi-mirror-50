import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aeon4py",
    version="0.0.3",
    author="Genesis",
    author_email="dev-genesis@ultimatesoftware.com",
    description="Aeon for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ultigit.ultimatesoftware.com/projects/VT/repos/aeon-python-client/browse",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['aeoncloud', 'py4j'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
