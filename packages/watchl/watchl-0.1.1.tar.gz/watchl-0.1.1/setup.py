from setuptools import find_packages, setup
from pathlib import Path

with open(str(Path(".") / "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


setup(
    name="watchl",
    version="0.1.1",
    license="MIT",
    url="https://github.com/florimondmanca/watchl.git",
    description="Lightweight HTTP log monitoring and alerting tool",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Florimond Manca",
    author_email="florimond.manca@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    package_data={"watchl": ["py.typed"]},
    zip_safe=False,
    install_requires=["click>=7, <8", "python-json-logger"],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "codecov",
            "black",
            "pylint",
            "rope",
            "mypy",
        ]
    },
    python_requires=">=3.6",
    entry_points={"console_scripts": ["watchl=watchl.main:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
