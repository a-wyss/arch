from setuptools import find_packages, setup

setup(
    name='aa_utils',
    version='0.0.1',
    url="",
    author="Andreas Wyss",
    author_email="andreas.wyss@tg.ch",
    install_requires=[],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={}
)
