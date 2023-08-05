import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="otpy",
    version="0.0.1",
    author="l0rem1psum",
    description="Python package for OTP (One-Time Password)",
    long_description="This is a Python package to cater to all your needs for generatring and verifying OTP (One-Time Password).",
    long_description_content_type="text/markdown",
    url="https://github.com/l0rem1psum/OTPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)