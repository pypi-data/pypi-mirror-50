import setuptools

long_description = """This package implements Jeongwan Haah's algorithm for quantum signal processing as described in this 
[paper](https://arxiv.org/abs/1806.10236). It includes a step by step 
algorithm that decomposes periodic functions (often from quantum signal processing) into a product of primitive matrices,
represented as a list of angles. The algorithmic complexity is O(N<sup>3</sup> polylog(N/𝜺)) where N is the degree of the
periodic function and 𝜺 is the precision parameter. The runtime bottleneck is a polynomial rootfinding in step 2. Haah 
concludes that the error is at most the error input (=15𝜺).
DISCLAIMER: This is in initial investigation stages, and the usage is subject to change. 
"""

setuptools.setup(
        name="qspd",
        version="1.0.1",
        author="Andrew Childs",
        author_email="amchilds@umd.edu",
        description="Quantum Signal Processing Decomposition",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitlab.umiacs.umd.edu/amchilds/qspd",
        packages=setuptools.find_packages(),
        install_requires=[
            "mpmath", "sympy", "numpy", "matplotlib"
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
)
