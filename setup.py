from setuptools import setup, find_packages

setup(
    name='camxes',
    version='0.2',
    description='Python interface to camxes.',
    long_description=open('README.rst').read(),

    author='Dag Odenhall',
    author_email='dag.odenhall@gmail.com',
    license='Simplified BSD',
    url='https://github.com/dag/python-camxes',

    packages=find_packages(),
    include_package_data=True,
    install_requires=['LEPL'],
    zip_safe=False,

    tests_require=['Attest>=0.5'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='camxes.tests.all',
    use_2to3=True,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Java',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Text Processing :: Linguistic',
    ],
)
