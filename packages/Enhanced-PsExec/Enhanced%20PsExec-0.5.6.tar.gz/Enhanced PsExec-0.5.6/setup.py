from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='Enhanced PsExec',
    version='0.5.6',
    description='Perform miscellaneous operations on A remote computer with Enhanced PsExec',
    py_modules=["Epsexec"],
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/orishamir/",
    author="Ori Shamir",
    author_email="Epsexecnoreply@gmail.com",

    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: System :: Systems Administration",
        "Operating System :: Microsoft :: Windows"
    ]
)
