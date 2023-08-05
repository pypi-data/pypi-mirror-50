import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='hk-first-pypi-upload',
    version='0.1',
    scripts=['dokr'],
    author="Hao Kuang",
    author_email="kuanghaochina@gmail.com",
    description="An example of python packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
