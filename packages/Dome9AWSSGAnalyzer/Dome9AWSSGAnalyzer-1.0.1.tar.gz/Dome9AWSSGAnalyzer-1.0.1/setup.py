from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="Dome9AWSSGAnalyzer",
    version="1.0.1",
    description="Get AWS-SG Details to respond to incidents quickly.",
    long_description=long_description,
    keywords="Dome9, AWS, Security Groups, Dome9v2API",
    long_description_content_type="text/markdown",
    author="Nitin Sharma",
    author_email="ntnshrm87@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["SGAnalyzerApp"],
    include_package_data=True,
    install_requires=[
        "requests", "configparser"
    ],
)
