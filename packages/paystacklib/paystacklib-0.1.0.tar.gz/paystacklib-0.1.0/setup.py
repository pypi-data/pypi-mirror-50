import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = 'paystacklib',
    version = '0.1.0',
    author= 'Abimbola Adegun',
    author_email = 'abimbola.adegun@gmail.com',
    description = 'A Python implementation of the Paystack API',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/abimbola/paystack-lib-python',
    packages=setuptools.find_packages(),
    install_requires=['requests', 'dotmap>=1.3.8'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
