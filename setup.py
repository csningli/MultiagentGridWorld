
from setuptools import setup, find_packages

setup(name='nil_gridopt',
      version='0.0.1',
      description='Grid World Optimization.',
      url='https://github.com/csningli/GridWorldOptimization',
      author='NING Li',
      author_email='csningli@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['numpy', 'pygame', 'pycos']
)
