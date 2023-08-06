import setuptools

setuptools.setup(
    name='scicap',
    version='2019.8.3',
    author='scicapital',
    author_email='public@scicapital.com',
    description='futures tool',
    license='MIT Licence',
    url='http://scicapital.com',
    packages=setuptools.find_packages(),
    platforms='any',
    python_requires=">=3.6",
    install_requires=["pandas>=0.21.0"],
)
