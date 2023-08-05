import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "InterpretableMLWrappers",
    version = "0.0.2",
    author = "Emile Givental",
    author_email = "emilegivental@gmail.com",
    description="A selection of interpretable methods with logging and printouts",
    long_description=long_description,
    url="https://github.com/egivental/resetInterpretability",
    packages = [],
    install_requires = ['cplex', 'Prettytable', 'pandas', 'numpy', 'sklearn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"
    ],

    )

