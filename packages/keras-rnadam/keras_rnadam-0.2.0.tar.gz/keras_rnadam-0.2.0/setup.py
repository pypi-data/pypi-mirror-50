import codecs
from setuptools import setup, find_packages

with codecs.open('README.md', 'r', 'utf8') as reader:
    long_description = reader.read()


setup(
    name='keras_rnadam',
    version='0.2.0',
    packages=['keras_rnadam'],
    url='https://github.com/niley1nov/keras_rnadam/archive/0.2.0.tar.gz',
    license='MIT',
    author='niley1nov',
    author_email='nilaysharma1nov@gmail.com',
    description='Rectified Nadam implemented in Keras',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
            "keras"
    ],
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

