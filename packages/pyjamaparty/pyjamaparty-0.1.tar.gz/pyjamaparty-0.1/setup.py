from setuptools import setup, find_packages

description = 'Set of casual python utilities'
long_description = '{}, written standing on shoulders of giants'.format(description)

requirements = []
setup(
   name='pyjamaparty',
   version='0.1',
   description=description,
   license="MIT",
   long_description=long_description,
   author='Karthik Rajasekaran',
   author_email='krajasek@gmail.com',
   url="http://github.com/krajasek/pyjamaparty",
   install_requires=requirements,
   packages=find_packages(exclude=('pyjamaparty.tests',)),
   python_requires='>=2.7'
)