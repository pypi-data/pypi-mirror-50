from setuptools import setup
print("\n\n\n\n\n hello!!!!\n\n")
with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='Enhanced PsExec',
    version='0.6.5',
    description='Perform miscellaneous operations on A remote computer with Enhanced PsExec',
    py_modules=["epsexec"],
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/orishamir/",
    author="Ori Shamir",
    author_email="Epsexecnoreply@gmail.com",

    install_requires=requirements,

    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: System :: Systems Administration",
        "Operating System :: Microsoft :: Windows"
    ]
)
