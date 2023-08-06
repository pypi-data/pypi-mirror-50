import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'dxql == 0.0.2',
    'click >= 7.0',
]

tests_require = [
    'pytest >= 5.0.1',
    'pytest-cov >= 2.7.1',
    'codecov >= 2.0.15',
]

setup(
    name='datax',
    version='0.0.1',
    description='DataXplorer ',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
    ],
    author='Eric Frechette',
    author_email='frechetta93@gmail.com',
    url='https://github.com/Frechetta/DataXplorer',
    keywords='data search query',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    python_requires='>= 3.7',
    long_description_content_type='text/markdown',
    entry_points = {
        'console_scripts': ['dx=datax.runner:run']
    },
)
