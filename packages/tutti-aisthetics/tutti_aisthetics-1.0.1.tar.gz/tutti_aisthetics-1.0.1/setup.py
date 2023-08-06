from setuptools import find_packages, setup
from tutti_aisthetics import __version__

setup(
    name='tutti_aisthetics',
    version=__version__,
    description='A tutti.ch image asthetics AI scorer.',
    long_description='Package based on https://github.com/idealo/image-quality-assessment.',
    author='Oscar Saleta',
    author_email='oscar@tutti.ch',
    license='Proprietary',
    keywords=['nima', 'CNN', 'neural net', 'MobileNet', 'aesthetics'],
    # package_dir={'': 'src'},
    packages=find_packages(exclude=['build', 'dist', '*test*']),
    python_requires='>=3.5.2',
    install_requires=[
        'keras==2.2.*',
        'absl-py==0.7.*',
        'tensorflow==1.14.*',
        'pillow==6.1.*',
        'plac==1.1.*',
        'boto3==1.9.*',
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
