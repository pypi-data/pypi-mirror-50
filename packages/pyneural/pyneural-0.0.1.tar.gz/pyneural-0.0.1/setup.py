import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(name = 'pyneural', version = '0.0.1', packages = ['pyneural'], install_requires = [], long_description = README, long_description_content_type = 'text/markdown',description = 'Library for brain modeling and machine learning in Python 3',classifiers = ['Development Status :: 2 - Pre-Alpha', 'Topic :: Scientific/Engineering :: Artificial Intelligence', 'Topic :: Scientific/Engineering :: Artificial Life', 'Topic :: Scientific/Engineering :: Bio-Informatics', 'Programming Language :: Python :: 3'],license = 'MIT',author = 'Tim Crimmins',author_email = 'tim.g.crimmins@gmail.com',include_package_data = True)
