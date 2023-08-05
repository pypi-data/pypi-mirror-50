from setuptools import setup

setup(
    name="tox-wikimedia",
    version="0.0.2",
    author="Kunal Mehta",
    author_email="legoktm@member.fsf.org",
    description="Automatically configure tox environments to use "
                "Wikimedia's standard tools",
    long_description=open("README.rst").read(),
    url="https://www.mediawiki.org/wiki/tox-wikimedia",
    packages=["tox_wikimedia"],
    entry_points={"tox": ["wikimedia = tox_wikimedia"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Framework :: tox",
        "License :: OSI Approved :: GNU General Public License v3 "
        "or later (GPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["tox>=3.8.0"],
)
