from setuptools import setup, find_packages

setup(
    name="cx",
    version="0.1.0",
    install_requires=["ccxt"],
    packages=find_packages(),
    entry_points={"console_scripts": ["cx=cx:main"]},
)
