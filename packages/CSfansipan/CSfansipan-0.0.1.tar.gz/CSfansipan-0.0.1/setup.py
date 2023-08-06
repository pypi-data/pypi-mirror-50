import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CSfansipan",
    version="0.0.1",
    author="Nguyen Minh Anh",
    author_email="minhanh@coderschool.vn",
    description="Coderschool's Full-time MLE package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minhanhng-cd/ftmle-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)