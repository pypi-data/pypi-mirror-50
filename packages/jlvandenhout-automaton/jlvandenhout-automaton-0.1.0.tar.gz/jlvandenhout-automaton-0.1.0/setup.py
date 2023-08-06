from setuptools import setup


with open("README.md") as f:
    long_description = f.read()


setup(
    name="jlvandenhout-automaton",
    version="0.1.0",
    author="J.L. van den Hout",
    packages=["jlvandenhout.automaton"],
    description="This package provides a simple automaton implementation for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jlvandenhout/automaton",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["jlvandenhout-graph>=2.0"],
)
