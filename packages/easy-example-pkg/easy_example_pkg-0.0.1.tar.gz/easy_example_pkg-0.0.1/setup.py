import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'easy_example_pkg',
    version = '0.0.1',
    author="chen955",
    author_email="zk__Chen@163.com",
    description="A A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chen955/AI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)