from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='text2output',
    version='1.0.5',
    description='Convert your text to print function in any language',
    py_modules=["text2output"],
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/orishamir/",
    author="Ori Shamir",

    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Artistic Software",
        "Operating System :: OS Independent"
    ]
)
