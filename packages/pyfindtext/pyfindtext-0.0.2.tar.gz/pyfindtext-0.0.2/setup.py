from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyfindtext',
    version='0.0.2',
    packages=['pyfindtext'],
    url='https://github.com/lagliam/pyfindtext',
    license='GNU General Public License v3.0',
    author='Liam Goring',
    description='Find text in files',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
