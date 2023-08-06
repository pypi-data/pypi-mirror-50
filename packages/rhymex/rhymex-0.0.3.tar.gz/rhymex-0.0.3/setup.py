import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rhymex",
    version="0.0.3",
    author="Max Nedelchev",
    author_email="max.nedelchev@gmail.com",
    description="Rhymex: library for analyzing russian words. Finding syllabuses and stresses in words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/MaxN/rhymex",
    packages=setuptools.find_packages(),
    include_package_data=True,  
    package_data={
        'rhymex': ['model/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)