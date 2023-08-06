from distutils.core import setup
setup(
  name = 'matialvarezs_charge_controller',
  packages = ['matialvarezs_charge_controller'], # this must be the same as the name above
  version = '0.0.108',
  install_requires = [
    'matialvarezs-handlers-easy==0.1.26',
    'python-crontab==2.3.6'
  ],
  include_package_data = True,
  description = 'Charge controller data',
  author = 'Matias Alvarez Sabate',
  author_email = 'matialvarezs@gmail.com',  
  classifiers = [
    'Programming Language :: Python :: 3.5',
  ],
)