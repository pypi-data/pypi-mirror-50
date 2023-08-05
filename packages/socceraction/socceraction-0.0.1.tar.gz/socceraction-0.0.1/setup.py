import setuptools

setuptools.setup(name='socceraction',
      version='0.0.1',
      description='Convert soccer event stream data to the SPADL format and value on-the-ball player actions in soccer',
      url='http://github.com/tomdecroos/matplotsoccer',
      author='Tom Decroos',
      author_email='tom.decroos.be@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
     install_requires = [
       "tqdm",
       "ujson",
       "pandas",
       "numpy",
       "unidecode"],
     long_description=open('docs/README_pip.md').read(),
     long_description_content_type='text/markdown',
      )