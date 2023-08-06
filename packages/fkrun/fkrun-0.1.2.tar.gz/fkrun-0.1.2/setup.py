from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='fkrun',
      version='0.1.2',
      packages=['fkrun'],
      author="Rudolfxx",
      author_email="mayeoliver@163.com",
      description="Code copier for multi experiments",
      long_description=long_description,
      long_description_content_type="text/markdown",
      entry_points={
          'console_scripts': [
              'fkrun = fkrun.__main__:main'
          ]
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      )
