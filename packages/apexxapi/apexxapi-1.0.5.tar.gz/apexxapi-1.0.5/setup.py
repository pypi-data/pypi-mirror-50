import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apexxapi",
    version="1.0.5",
    author="Hugo Wickham",
    author_email="hugo.wickham@apexx.global",
    description="Package containing functions for accessing Apexx API 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HugoWickham/apexxpython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
