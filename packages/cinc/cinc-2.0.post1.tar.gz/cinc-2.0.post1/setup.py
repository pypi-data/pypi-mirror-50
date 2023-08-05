from setuptools import setup, Extension


with open('README.rst') as f:
    readme = f.read()


setup(
    name='cinc',
    version='2.0',

    py_modules=['cinc'],
    ext_modules=[Extension('cinc', ['cinc.cpp'], optional=True)],

    test_suite='testcases',
    tests_require=['dualtest'],

    description='Fast fixed-sized C-like integer types.',
    long_description=readme,
    url='https://pypi.org/project/cinc/',
    author='Mark Sierak',
    author_email='mZarjk_@mailfence.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
