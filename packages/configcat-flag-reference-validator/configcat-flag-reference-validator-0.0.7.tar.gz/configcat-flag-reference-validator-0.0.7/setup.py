import setuptools


def readme():
    with open('README.md') as f:
        return f.read()


version = "0.0.7"


setuptools.setup(
    name='configcat-flag-reference-validator',
    version=version,
    scripts=['configcat-validator'],
    packages=['configcat', 'configcat.reference_validator'],
    url='https://github.com/configcat/flag-reference-validator',
    license='MIT',
    author='ConfigCat',
    author_email='developer@configcat.com',
    description='ConfigCat flag reference validator.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=['requests>=2.19.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)