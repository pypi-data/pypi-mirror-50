from setuptools import find_packages, setup

setup(
    name='cmu-multimodal-sdk',
    version='0.0.6',
    description='a copy of cmu-multimodal-sdk',
    author='Lec',
    author_email='2524463910@qq.com',
    url='https://github.com/lizhaoliu-Lec/CMU-MultimodalSDK',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.17.0',
        'requests>=2.22.0',
        'validators>=0.13.0',
        'h5py>=2.9.0',
        'tqdm>=4.33.0',
        'setuptools>=41.0.1',
        'six>=1.12.0',
    ],
)
