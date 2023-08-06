import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements_list = fh.read().splitlines()

setuptools.setup(
    name='ssid_scanner',
    version='0.1.0',
    author='ae-ou',
    description='A package for scanning nearby wireless access points on Linux machines.',
    install_requires=requirements_list,
    long_description=long_description,
    url='https://gitlab.com/ae-ou/ssid_scanner',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'License :: Other/Proprietary License',
        'Topic :: System :: Networking',
    ],
)
