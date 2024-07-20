from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

NAME = "integration-suite"
VERSION = "1.0.0"


def pre_install_script():
    subprocess.run(["bash", "./scripts/generate-models.sh"])


class CustomInstallCommand(install):
    def run(self):
        pre_install_script()
        install.run(self)


setup(
    name=NAME,
    version=VERSION,
    description="The integration suite for the Aparavi application.",
    keywords=["integration", "suite", "aparavi"],
    cmdclass={
        'install': CustomInstallCommand
    },
    install_requires=open("requirements.txt").readlines(),
    packages=find_packages(),
    options={
        'egg_info': {'egg_base': './build'}
    },
)
