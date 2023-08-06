from setuptools import setup, find_packages

setup(
    name='QuickWall',
    packages=find_packages(),
    author='Deepjyoti Barman',
    author_email='deep.barman30@gmail.com',
    description='Set any wallpaper from commandline',
    long_description='Set any wallpaper from Unsplash from the commandline',
    url='http://github.com/deepjyoti30/quickwall',
    scripts=['scripts/QuickWall'],
    version='0.0.1-2',
    license='MIT',
    install_requires=['requests'],
)
