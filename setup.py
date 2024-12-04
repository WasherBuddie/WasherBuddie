from setuptools import setup, find_packages

# This setup.py is mainly for backward compatibility
# Most configuration is handled in pyproject.toml

setup(
    name="washerbuddie",
    packages=find_packages(include=['Service_Layer', 'Service_Layer.*']),
    package_dir={'': 'src'},
    install_requires=[
        'python-dateutil>=2.8.2',
    ],
    extras_require={
        'test': [
            'pytest>=7.4.3',
            'pytest-cov>=4.1.0',
        ],
    },
)