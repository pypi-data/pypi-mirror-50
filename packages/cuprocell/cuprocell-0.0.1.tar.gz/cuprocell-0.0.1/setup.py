import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name='cuprocell',
    version='0.0.1',
    description="Python wrapper for CUDA C++ ProCell implementation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ericniso/py-cuprocell",
    author="Eric Nisoli",
    author_email="e.nisoli1@campus.unimib.it",
    license="GPL-3.0",
    classifiers=[],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[],
    scripts=['bin/cuprocell-install.sh', 'bin/cuprocell-install.bat'],
)
