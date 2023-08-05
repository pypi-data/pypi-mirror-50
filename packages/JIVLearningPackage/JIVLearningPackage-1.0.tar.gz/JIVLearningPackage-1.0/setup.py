import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JIVLearningPackage",
    version=1.0,
    author_email = "m.johnmarshal@gmail.com",
    description="Learning process",
    long_description = long_description,
    long_description_content_type='text/markdown',
    packages = setuptools.find_packages(exclude=["tests", "data"]) 
)
