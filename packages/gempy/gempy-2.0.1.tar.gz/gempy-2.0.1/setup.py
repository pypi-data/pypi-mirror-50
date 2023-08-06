from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gempy',
    version='2.0.1',
    packages=find_packages(exclude=('test', 'docs')),
    include_package_data=True,
    install_requires=[
        'cython',
        'numpy',
        'pandas',
        'matplotlib',
        'theano',
        'scikit-image',
        'seaborn'
    ],
    url='https://github.com/cgre-aachen/gempy',
    download_url='https://github.com/cgre-aachen/gempy/archive/2.0.0tar.gz',
    license='LGPL v3',
    author='Miguel de la Varga, Elisa Heim, Alexander Schaaf, Fabian Stamm, Florian Wellmann',
    author_email='varga@aices.rwth-aachen.de',
    description='An Open-source, Python-based 3-D structural geological modeling software.',
    keywords=['geology', '3-D modeling', 'structural geology', 'uncertainty']
)
