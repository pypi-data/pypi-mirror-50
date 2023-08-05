from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="deepvission-nightly",
    version="1.0.1",
    description="Python package for Deep Neural Netrwork Pre-trained Model testing.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/suvhradipghosh07/deepvision",
    author="Suvhradip Ghosh",
    author_email="suvhradip.ai@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["deepvission"],
    include_package_data=True,
    install_requires=["requests","keras","tensorflow","opencv-python","Pillow","numpy"]
)