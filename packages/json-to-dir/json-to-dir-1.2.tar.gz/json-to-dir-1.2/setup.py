import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json-to-dir",
    version="1.2",
    author="fiatjaf",
    author_email="fiatjaf@gmail.com",
    license="MIT",
    description="Turns a JSON file into a directory structure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[],
    scripts=["json-to-dir"],
)
