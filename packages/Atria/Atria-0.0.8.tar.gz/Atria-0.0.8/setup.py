import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="Atria",
    version="0.0.8",
    author="RedDog",
    author_email="bremo.lincolin101@gmail.com",
    description="A simple messaging bot for python",
    long_description=description,
    url="https://github.com/RedDogCode/Atria",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ]
)
