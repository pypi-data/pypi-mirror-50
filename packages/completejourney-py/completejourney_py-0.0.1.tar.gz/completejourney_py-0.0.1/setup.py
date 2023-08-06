from setuptools import setup, find_packages

setup(
    name='completejourney_py',
    version='0.0.1',
    description='Data from R package completejourney',
    author='James Cunningham',
    author_email='james@notbadafterall.com',
    packages=find_packages(include=['completejourney_py', 'completejourney_py.*']),
    install_requires=['pandas>=0.25.0'],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    package_data={'completejourney_py': ['data/*.parquet']}
)
