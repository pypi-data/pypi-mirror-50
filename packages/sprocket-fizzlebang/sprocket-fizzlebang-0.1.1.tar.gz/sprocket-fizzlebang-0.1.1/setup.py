import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sprocket-fizzlebang",
    version="0.1.1",
    author="Chase Franklin",
    author_email="gnullbyte@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnullbyte/sprocket",
    packages=setuptools.find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=["dicey", "discord.py"],
    entry_points={"console_scripts": ["sprocket=sprocket.__main__:run"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
