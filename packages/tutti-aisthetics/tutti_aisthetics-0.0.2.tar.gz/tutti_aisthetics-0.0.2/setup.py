from setuptools import setup, find_packages
from src.tutti_aisthetics import __version__

setup(
    name='tutti_aisthetics',
    version=__version__,
    description='A tutti.ch image asthetics AI scorer.',
    long_description='Package based on https://github.com/idealo/image-quality-assessment.',
    author='Oscar Saleta',
    author_email='oscar@tutti.ch',
    license='Proprietary',
    keywords=['nima', 'CNN', 'neural net', 'MobileNet', 'aesthetics'],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5.2',
    install_requires=[
        'pandas==0.25.*',
        'keras==2.1.*',
        'nose==1.3.*',
        'pillow==5.0.*',
        'plac==1.0.0',
        'awscli==1.16.*',
        'boto3==1.5.*',
        'botocore==1.12.*',
    ],
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    package_data={
        'tutti_aisthetics': ['model/*.hdf5']
    },
    include_package_data=True
)
