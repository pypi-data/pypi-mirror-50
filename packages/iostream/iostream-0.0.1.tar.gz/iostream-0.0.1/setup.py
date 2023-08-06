from setuptools import setup,find_packages
setup(
    name='iostream',
    version='0.0.1',
    author='CubieLee',
    author_email='liyixiao0608@gmail.com',
    description='iostream for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://lyx.sanqqq.com',
    packages=find_packages(),
    install_requires=[
        'pywin32'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
    ],
)
