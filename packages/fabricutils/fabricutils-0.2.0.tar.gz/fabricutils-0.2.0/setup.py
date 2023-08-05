import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()


setup(
    name='fabricutils',
    version='0.2.0',
    description='Fabric helper utilities',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/makukha/fabricutils',
    author='Michael Makukha',
    author_email='m.makukha@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        ],
    packages=['.'],
    install_requires=['fabric>=2.4.0'],
    )
