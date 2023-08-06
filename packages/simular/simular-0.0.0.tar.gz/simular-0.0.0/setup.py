"""
Placeholder for future development
"""
from setuptools import find_packages
from setuptools import setup

dependencies = ['click']

setup(
    name='simular',
    version='0.0.0',
    url='https://github.com/thumperrr/simular',
    license='MIT',
    author='Steve Hall',
    author_email='hallsb808@gmail.com',
    description='Dynamics and Vehicle Simulation',
    long_description=__doc__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
#            'simular = simular.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Scientific/Engineering'
    ],
    project_urls={
            'Changelog': 'https://github.com/thumperrr/simular/blob/master/CHANGELOG.rst',
            'Issue Tracker': 'https://github.com/thumperrr/simular/issues',
        }
)
