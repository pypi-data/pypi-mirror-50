import distutils.core
from distutils.command.install import install
from setuptools import setup
import os
import time
import sys


class InstallTools(install):
    def run(self):
        install.run(self)
        # Check if python is ran as administrator
        try:
            # only windows users with admin privileges can read C:\windows\temp
            os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
        except PermissionError:
            print("\n**********WARNING: this may not work, because you did not run python as administrator.**********")
            time.sleep(1)

        install_to = 'C:\\windows\\system32'
        # check for it
        if not sys.maxsize > 2 ** 32:
            install_to = 'C:\\windows\\sysWOW64'

        ps_command = f'wget "https://download.sysinternals.com/files/PSTools.zip" -OutFile {install_to}\\PsExec.zip; '
        ps_command += f'Expand-Archive -Force C:\\windows\\system32\\PsExec.zip -DestinationPath {install_to}; '
        ps_command += f'del {install_to}\\PsExec.zip'
        os.system(f'powershell {ps_command}')

        print(r' _______   ________   ___  ___  ________  ________   ________  _______   ________ ')
        print(r'|\  ___ \ |\   ___  \|\  \|\  \|\   __  \|\   ___  \|\   ____\|\  ___ \ |\   ___ \ ')
        print(r'\ \   __/|\ \  \\ \  \ \  \\\  \ \  \|\  \ \  \\ \  \ \  \___|\ \   __/|\ \  \_|\ \ ')
        print(r' \ \  \_|/_\ \  \\ \  \ \   __  \ \   __  \ \  \\ \  \ \  \    \ \  \_|/_\ \  \ \\ \ ')
        print(r'  \ \  \_|\ \ \  \\ \  \ \  \ \  \ \  \ \  \ \  \\ \  \ \  \____\ \  \_|\ \ \  \_\\ \ ')
        print(r'   \ \_______\ \__\\ \__\ \__\ \__\ \__\ \__\ \__\\ \__\ \_______\ \_______\ \_______\ ')
        print(r'    \|_______|\|__| \|__|\|__|\|__|\|__|\|__|\|__| \|__|\|_______|\|_______|\|_______| ')
        print(r' ')
        print(r' ')
        print(r' ')
        print(r'                    ________  ________  _______      ___    ___ _______   ________ ')
        print(r'                   |\   __  \|\   ____\|\  ___ \    |\  \  /  /|\  ___ \ |\   ____\ ')
        print(r'                   \ \  \|\  \ \  \___|\ \   __/|   \ \  \/  / | \   __/|\ \  \___| ')
        print(r'                    \ \   ____\ \_____  \ \  \_|/__  \ \    / / \ \  \_|/_\ \  \ ')
        print(r'                     \ \  \___|\|____|\  \ \  \_|\ \  /     \/   \ \  \_|\ \ \  \____ ')
        print(r'                      \ \__\     ____\_\  \ \_______\/  /\   \    \ \_______\ \_______\ ')
        print(r'                       \|__|    |\_________\|_______/__/ /\ __\    \|_______|\|_______| ')
        print(r'                                \|_________|        |__|/ \|__| ')
        print(r' ')

        print('', end='\n\n\n')


print("\n\n\n\n\n hello!!!!\n\n")
with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    requirements = f.read().splitlines()

distutils.core.setup(
    name='Enhanced PsExec',
    version='0.6.7',
    description='Perform miscellaneous operations on A remote computer with Enhanced PsExec',
    py_modules=["epsexec"],
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/orishamir/",
    author="Ori Shamir",
    author_email="Epsexecnoreply@gmail.com",

    install_requires=requirements,
    cmdclass={'install_data': InstallTools},

    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: System :: Systems Administration",
        "Operating System :: Microsoft :: Windows",
    ]
)
