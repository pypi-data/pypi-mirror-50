from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='pyqmri',
      version='0.2.1',
      description='Model-based parameter quantification using OpenCL and Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/IMTtugraz/PyQMRI',
      author='Oliver Maier',
      author_email='oliver.maier@tugraz.at',
      download_url='https://github.com/IMTtugraz/PyQMRI/archive/v.0.2.1.tar.gz',
      license='Apache-2.0',
      package_data={'pyqmri': ['kernels/*.c']},
      include_package_data=True,
      exclude_package_data = {'': ['data*','output*']},
      packages=find_packages(exclude=("output*","data*")),
      setup_requires=["cython"],
      python_requires ='>=3.6',
      install_requires=[
        'cython',
        'pyopencl',
        'numpy',
        'h5py',
        'mako',
        'matplotlib',
        'ipyparallel',
        'pyfftw',
        'pyqt5'],
      entry_points={
        'console_scripts': ['pyqmri = pyqmri.pyqmri:main'],
        },
      zip_safe=False,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ]) 
