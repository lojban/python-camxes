from setuptools import setup, find_packages

setup(name='camxes',
      version='0.1',
      packages=find_packages(),
      package_data={'camxes': ['camxes.jar']},
      install_requires=['lepl'],
      tests_require=['attest>=0.5'],
      test_loader='attest:auto_reporter.test_loader',
      test_suite='camxes.tests.all',
      use_2to3=True,
     )
