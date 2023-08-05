#from distutils.core import setup

#setup(
#    name='PyCDTS',
#    version='0.1.0',
#    author='Abdul Rawoof Shaik',
#    author_email='arshaik@asu.edu',
#    packages=['pycdts', 'pycdts.test'],
##    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
#    url='http://pypi.python.org/pypi/PyCDTS/',
#    license='LICENSE.txt',
#    description='A Python based Carrier and Defect Transport Solver',
#    long_description=open('README.txt').read(),
#    install_requires=[
#        "PyQt5  >=5.9.2",
#        "scikit-umfpack >=0.3.1"
#    ],
#)

import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCDTS",
    version="0.2.0",
    author="Abdul Rawoof Shaik",
    author_email="arshaik@asu.edu",
    description="A Python based Carrier and Defect Transport Solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abdul529/pycdts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
         'numpy >= 1.16.3',
         'scipy >= 1.2.1',
         'matplotlib >= 3.0.3',
         'PyQt5  >= 5.9.2',
         'scikit-umfpack >= 0.3.1',
         'pyqtgraph >= 0.10.0',
         'h5py >= 2.9.0',
         'PyOpenGL >=3.1.0',
    ],  
    scripts=['bin/cdts.py'],
)
