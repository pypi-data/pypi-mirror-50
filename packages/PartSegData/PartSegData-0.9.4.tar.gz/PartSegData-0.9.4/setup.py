import setuptools
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base_dir, "README.rst")) as ff:
    readme_text = ff.read()

setuptools.setup(
    name="PartSegData",
    version="0.9.4",
    author="Grzegorz Bokota",
    author_email="g.bokota@cent.uw.edu.pl",
    description="PartSeg data files",
    url="https://4dnucleome.cent.uw.edu.pl/PartSeg/",
    packages=["PartSegData"],
    include_package_data=True,
    long_description=readme_text,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
)
