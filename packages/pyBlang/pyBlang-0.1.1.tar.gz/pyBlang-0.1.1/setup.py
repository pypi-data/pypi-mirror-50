import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyBlang',
    version='0.1.1',
    packages=setuptools.find_packages(),
    url='',
    license='',
    author='Sahand Hosseini',
    author_email='',
    description='A python package to run Blang CLI commands and streamline usage through python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['matplotlib', 'seaborn', 'pandas', 'numpy']
)
