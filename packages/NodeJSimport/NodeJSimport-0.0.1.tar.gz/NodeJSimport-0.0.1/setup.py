from setuptools import setup
from Cython.Build import cythonize
setup(
    name="NodeJSimport",
    packages=["."],
    package_data={".":["NodeJSimport.py"]},
    install_requires=["js2py"],
    version="0.0.1"
)