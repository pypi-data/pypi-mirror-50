from setuptools import setup, find_packages

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

setup(
    name = "sc2-env",
    packages = find_packages(),
    version = "0.11.1",
    description = "A StarCraft II bot gym env library over python-sc2",
    license="MIT",
    author = "Damien GILLES",
    author_email = "damien.gilles.pro@gmail.com",
    url = "https://github.com/gillesdami/python-sc2",
    keywords = ["StarCraft", "StarCraft 2", "StarCraft II", "AI", "Bot"],
    setup_requires=["pipenv"],
    install_requires=requirements,
    classifiers = [
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
