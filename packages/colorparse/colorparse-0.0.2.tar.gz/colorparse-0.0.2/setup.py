import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='colorparse',
    version='0.0.2',
    author='Esteban Carrillo',
    author_email='estebancn0324@hotmail.com',
    description='A string-coloring package for terminals',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tubi-carrillo/colorparse',
    py_modules=['colorparse'],
    packages=setuptools.find_packages(),
    keywords='colorparse, terminal, color, ansi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        "console_scripts": ["colorparse=colorparse:_main"],
    },
)
