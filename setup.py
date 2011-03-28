from setuptools import setup

setup(name='camxes',
      version='0.1',
      install_requires=['lepl'],
      tests_require=['attest>=0.5'],
      test_loader='attest:auto_reporter.test_loader',
      test_suite='tests.all',
     )
