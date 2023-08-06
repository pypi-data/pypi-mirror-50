import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timerr",
    version="1.0.3",
    author="ItzAfroBoy",
    author_email="spareafro@post.com",
    description="A basic timer that counts down from time entered",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ItzAfroBoy/timerr",
    packages=setuptools.find_packages(),
    clssifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
