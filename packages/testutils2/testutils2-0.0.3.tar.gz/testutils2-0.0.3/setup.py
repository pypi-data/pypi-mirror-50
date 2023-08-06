import setuptools

#from client_side.eth_utils import EthUtils

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testutils2",
    version="0.0.3",
    author="Corp",
    author_email="id.justevolution@gmail.com",
    description="EthUtils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kefirock/ethutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
