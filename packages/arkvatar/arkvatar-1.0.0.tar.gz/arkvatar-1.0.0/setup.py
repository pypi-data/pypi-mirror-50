import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arkvatar",
    version="1.0.0",
    author="Jolan Beer - Highjhacker",
    author_email="jolanbeer@gmail.com",
    description="API Wrapper to interact with Arkvatar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thegoldenhorde/arkvatar-py",
    packages=['arkvatar'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    install_requires=[
        'aiohttp',
    ],
    python_requires=">=3",
    zip_safe=False
)
