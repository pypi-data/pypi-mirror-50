import setuptools

setuptools.setup(
    name="UnDupe",
    version="0.0.1",
    author="Andrew Xiao, Rajat Bapuri, Sean Nordquist",
    author_email="",
    description="Remove duplicate texts from a .txt file",
    long_description="Remove duplicate texts from a .txt file "
                     "by using cosine similarity to compare texts.",
    long_description_content_type="text/markdown",
    url="https://github.com/andrewsx/undupe.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tqdm >= 4.32.1'
    ]
)
