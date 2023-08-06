import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='injectslib',
    version='0.0.1',
    author="msm",
    author_email="msm@cert.pl",
    package_dir={'injectslib': 'src'},
    packages=['injectslib'],
    description="Official API package for https://injects.cert.pl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
