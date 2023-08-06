"""
Bear

bear is a pipeline allowing you to run tasks in parallel in such
a way that it truly uses multiple cores of your processor
It also allow resuming failed pipelines and profiling and monitoring tasks and system memory.
"""
from setuptools import Command, setup, find_packages

version = '2.0'
setup(
    name='bear',
    version=version,
    url='https://github.com/kouroshparsa/bear',
    download_url='https://github.com/kouroshparsa/bear/packages/%s' % version,
    license='GNU',
    author='Kourosh Parsa',
    author_email="kouroshtheking@gmail.com",
    description='asynchronous parallelization pipeline',
    long_description=__doc__,
    packages=find_packages(),
    install_requires = ['psutil', 'matplotlib', 'bunch'],
    include_package_data=True,
    package_data = {'bear': []},
    zip_safe=False,
    platforms='all',
    classifiers=[
        'Programming Language :: Python',
    ]
)
