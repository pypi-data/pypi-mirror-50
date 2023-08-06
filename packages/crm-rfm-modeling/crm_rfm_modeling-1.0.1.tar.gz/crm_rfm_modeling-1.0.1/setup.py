from distutils.core import setup
import setuptools
setup(
    name='crm_rfm_modeling',
    author='Juan Zarco',
    version='1.0.1',
    description='RFM (Recency Frequency Monetary) model python package',
    url='https://github.com/jzarco/RFM',
    packages=['crm_rfm_modeling'],
    install_requires=['pandas','numpy','datetime'],
    license='GNU General Public License',
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta'
    ],
)