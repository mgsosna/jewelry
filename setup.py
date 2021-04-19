from setuptools import setup, find_packages

NAME = 'jewelry'
URL = 'https://github.com/mgsosna/jewelry'
REQUIRES_PYTHON = '>=3.7.0'
REQUIREMENTS_FN = 'requirements.txt'


def list_requirements(file_name=REQUIREMENTS_FN):
    with open(file_name) as f:
        return f.read().splitlines()


setup(
    name=NAME,
    version="0.1.0",
    include_package_data=True,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    package_dir={'': 'jewelry'},
    packages=find_packages(where="jewelry"),
    install_requires=list_requirements()
)
