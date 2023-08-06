import setuptools


extras_require = {
    "test": [
        "codecov>=2.0.15,<3.0.0",
        "factory-boy>=2.12.0,<3.0.0",
        "pytest>=4.6.3,<5.0.0",
        "pytest-cov>=2.7.1,<3.0.0",
        "pytest-asyncio>=0.10.0,<1.0.0",
    ],
    "lint": ["mypy>=0.701,<1.0", "black>=19.3b0", "isort==4.3.21", "flake8>=3.7.7,<4.0.0"],
    "dev": ["tox>=3.13.2,<4.0.0"],
}

extras_require["dev"] = extras_require["test"] + extras_require["lint"] + extras_require["dev"]


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="yamux",
    description="yamux implementation written in python",
    version="0.0.1",
    license="MIT",
    author="Kevin Mai-Hsuan Chia",
    author_email="kevin@mhchia.com",
    url="https://github.com/mhchia/py-yamux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require=extras_require,
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
