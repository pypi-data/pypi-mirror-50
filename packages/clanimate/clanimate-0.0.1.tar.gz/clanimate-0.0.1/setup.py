import setuptools

with open('README.md', 'r') as readme_fp:
    long_description = readme_fp.read()


setuptools.setup(
    name='clanimate',
    description='A CLI loading bar and animation python library.',
    version='0.0.1',
    author='Jakub Wlodek',
    author_email='jwlodek.dev@gmail.com',
    long_description_content_type = 'text/markdown',
    license='BSD (3-clause)',
    packages=['clanimate'],
    url='https://github.com/jwlodek/clanimate',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',        
        'Programming Language :: Python :: 3.7',
    ],
    keywords='animation cli commandline progressbar',
    python_requires='>=3.2',
)
