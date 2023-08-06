import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'lark-parser==0.7.1'
]

tests_require = [
    'pytest >= 3.7.4',
    'pytest-cov',
]

setup(
    name='dxql',
    version='0.0.1',
    description='Data eXploration Query Language (DXQL)',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    author='Eric Frechette',
    author_email='frechetta93@gmail.com',
    url='https://github.com/Frechetta/DXQL',
    keywords='data search query language',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    python_requires='>= 3.7',
    long_description_content_type='text/markdown',
)
