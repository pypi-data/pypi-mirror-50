import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='torch-mtcnn',
    version='0.0.7',
    author='Dan Antoshchenko',
    description='Implementation of MTCNN using Pytorch.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khrlimam/mtcnn-pytorch",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'torch', 'torchvision'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
