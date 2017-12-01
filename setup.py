from setuptools import setup, find_packages
from ngi_analysis_manager import __version__

setup(
    name='ngi-analysis-manager',
    version=__version__,
    description="",
    long_description="",
    keywords=[],
    author='Pontus Larsson, SNP&SEQ Technology Platform, Uppsala University',
    author_email="",
    url="https://www.github.com/b97pla/ngi-analysis-manager",
    download_url="",
    install_requires=[],
    packages=find_packages(exclude=["tests*"]),
    test_suite="tests",
    package_data={},
    include_package_data=True,
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
