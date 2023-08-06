import setuptools
from tutti_aisthetics_slim import __version__

setuptools.setup(
    name='tutti_aisthetics_slim',
    version=__version__,
    description='A tutti.ch image asthetics AI scorer.',
    long_description='Stripped down version of package tutti-aisthetics for pure Tensorflow inference.',
    author='Oscar Saleta',
    author_email='oscar@tutti.ch',
    url='https://tutti.ch',
    license='Proprietary',
    keywords=['nima', 'CNN', 'neural net', 'MobileNet', 'aesthetics'],
    packages=setuptools.find_packages(exclude=['build', 'dist', '*test*']),
    python_requires='>=3.5.2',
    install_requires=[
        'absl-py==0.7.*',
        'boto3==1.9.*',
        'pillow==6.1.*',
        'tensorflow==1.14.*',
    ],
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    package_data={
        'tutti_aisthetics_slim': ['model/model.pb']
    },
    include_package_data=True
)
