# Import SetupTools Module
import setuptools
# From PathLib Object Import Path Class
from pathlib import Path

# Use .setup() Method and Pass Arguments
setuptools.setup(
    name="bndoug66.pdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["Test", "Data"])
)
