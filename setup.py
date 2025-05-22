from setuptools import setup
from setuptools import find_packages

# find_packages will find all the packages with __init__.py
print(find_packages())

setup(
    name="yh-dashboard",
    version="0.0.1",
    description="""
    This package is used for creating a dashboard in taipy
    """,
    author="Grupp 4",
    author_email="moghadasi.64@gmail.com",
    install_requires=["pandas", "taipy", "duckdb"],
    packages=find_packages(exclude=("test*", "EDA_filer", "files")),
)