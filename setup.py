from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="mkdocs-exclude-search",
    version="0.5.0",
    description="A mkdocs plugin that lets you exclude selected files or sections "
    "from the search index.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="mkdocs",
    url="https://github.com/chrieke/mkdocs-exclude-search",
    author="Christoph Rieke",
    author_email="christoph.k.rieke@gmail.com",
    license="MIT",
    python_requires=">=2.7",
    install_requires=["mkdocs>=1.0.4"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": ["exclude-search = mkdocs_exclude_search:ExcludeSearch"]
    },
)
