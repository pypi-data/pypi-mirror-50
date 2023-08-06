import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tabout",
    version="1.0.2",
    author="Dan Averbuj",
    author_email="dan.averbuj@gmail.com",
    description="Create sound and/or slack notifications within your script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daverbuj/Tabout",
    packages=setuptools.find_packages(),
    install_requires=['playsound', 'slackclient', 'pox']
)
