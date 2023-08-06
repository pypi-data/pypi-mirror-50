from distutils.core import setup
setup(
    name='fgdtools',
    packages=['fgdtools'],
    version='0.2.0',
    license='gpl-3.0',
    description='A library to parse .fgd files used in the source engine.',
    author='Maxime Dupuis',
    author_email='mdupuis@hotmail.ca',
    url='https://maxdup.github.io/fgd-tools/',
    download_url='https://github.com/maxdup/fgd-tools/archive/v0.2.0.tar.gz',
    keywords=['fgd', 'source', 'hammer'],
    install_requires=['pyparsing'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
