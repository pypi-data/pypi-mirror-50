import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="augmentation_lib",
    version="0.0.1",
    author="Laura Lu",
    author_email="new4spam@gmail.com",
    description="Image augmentation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laume/augmentation_lib",
    download_url="https://github.com/laume/augmentation_lib",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "Pillow",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)