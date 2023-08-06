from setuptools import find_packages, setup


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name="deluxe",
    version="0.0.0",
    author="Bulat Bochkariov",
    author_email="bulat+pypi@bochkariov.com",
    description="Deluxe configuration management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
    ]
)
