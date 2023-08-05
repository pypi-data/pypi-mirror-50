import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simple-json-logging',
    version='1.0.5',
    license='MIT',
    author='Sergey Nevmerzhitsky',
    author_email='sergey.nevmerzhitsky@gmail.com',
    description='Library for structured logging via JSON document',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nevmerzhitsky/python-simple-json-logging',
    keywords=['logging', 'json'],
    python_requires='~=3.7',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
