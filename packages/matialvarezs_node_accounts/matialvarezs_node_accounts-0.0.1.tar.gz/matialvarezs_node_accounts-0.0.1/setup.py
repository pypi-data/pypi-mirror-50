from distutils.core import setup
import setuptools
setuptools.setup(
  name = 'matialvarezs_node_accounts',
  packages = setuptools.find_packages(),#['matialvarezs_node_configurations'], # this must be the same as the name above
  version = '0.0.1',
  install_requires = [

  ],
  include_package_data = True,
  description = 'Nodes accounts - create user api and get token',
  author = 'Matias Alvarez Sabate',
  author_email = 'matialvarezs@gmail.com',  
  classifiers = [
    'Programming Language :: Python :: 3.5',
  ],
)