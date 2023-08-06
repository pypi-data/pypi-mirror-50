from setuptools import setup, find_packages

setup(
    name="twelve_step",
    packages=find_packages(exclude=["*test*"]),
    version="0.0.6",
    license="MIT",
    description="A package to analyze project dependencies.",
    author="Olivier Beaulieu",
    author_email="beaulieu.olivier@hotmail.com",
    url="https://github.com/OLBEA20/twelve-step",
    download_url="https://github.com/OLBEA20/twelve-step/archive/0.0.6.tar.gz",
    keywords=["Dependency", "Analysis", "Dependencies", "Graph"],
    install_requires=["jivago-streams"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["twelve-step=twelve_step.main:main"]},
)
