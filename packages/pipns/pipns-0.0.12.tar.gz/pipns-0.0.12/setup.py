import setuptools

setuptools.setup(
    name='pipns',
    version='0.0.12',
    author='Andrew Rabert',
    author_email='ar@nullsum.net',
    url='https://github.com/nvllsvm/pipns',
    license='MIT',
    packages=['pipns'],
    entry_points={'console_scripts': ['pipns=pipns.__main__:main']},
    package_data={'pipns': ['scripts/*.py']},
    install_requires=['pipenv'],
    python_requires='>=3.7')
