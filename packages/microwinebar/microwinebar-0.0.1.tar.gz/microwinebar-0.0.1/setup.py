from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='microwinebar',
    version='0.0.1',
    description='MicroWineBar',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='klincke',
    author_email='franziska.klincke@bio.ku.dk',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: MacOS",
        'Operating System :: POSIX',
        'Operating System :: Unix',
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics"],
    LICENSE='MIT',
    url='https://github.com/klincke/microwinebar',
    #install_requires=['openpyxl', 'numpy', 'pandas', 'scipy', 'scikit-learn', 'scikit-bio', 'wikipedia', 'Pmw', 'matplotlib', 'seaborn'],
    install_requires=['matplotlib==2.2.3', 'openpyxl==2.6.0', 'numpy==1.16.4', 'pandas==0.24.2', 'scipy==1.3.0', 'scikit-learn==0.21.2', 'scikit-bio==0.5.5', 'wikipedia==1.4.0', 'Pmw==2.0.1', 'seaborn'],
    entry_points={'console_scripts':['microwinebar = microwinebar.microwinebar:main']}
)
