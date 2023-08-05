import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(name = 'timshive', version = '0.1.0', packages = ['timshive'], install_requires = ['matplotlib','numpy'], long_description = README, long_description_content_type = 'text/markdown',description = 'Program for creating simple hive plots in python using multidimensional arrays.',classifiers = ['Development Status :: 4 - Beta', 'Topic :: Scientific/Engineering :: Visualization', 'Programming Language :: Python :: 3'],license = 'MIT',author = 'Tim Crimmins',author_email = 'tim.g.crimmins@gmail.com')
