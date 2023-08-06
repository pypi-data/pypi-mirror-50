import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="belousov-zhabotinsky",
    version="0.6.1",
    author="Lucas Stefan Minuzzi Neumann",
    author_email="neumannmlucas@gmail.com",
    description="Simulation of the Belousov-Zhabotinski reaction using ASCII art",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neumann-mlucas/belousov-zhabotinsky",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['belousov-zhabotinsky=belousov_zhabotinsky.main:main']
    },
    python_requires='>=3',
    install_requires=['numpy', 'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
