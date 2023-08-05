import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read()

setuptools.setup(
    name='notarius',
    version=version,
    scripts=['notarius'],
    author='Jean-Francois Theroux',
    author_email='jftheroux@devolutions.net',
    description='Tool to notarize a macOS dmg',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Devolutions/notarius',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
    ],
)
