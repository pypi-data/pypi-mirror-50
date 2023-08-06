from setuptools import setup
setup(
    name = 'pclimate',
    version = '0.1.0',
    packages = ['pclimate'],
    entry_points = {
        'console_scripts': [
            'pclimate = pclimate.__main__:main'
        ]
    },
    description = "Simple CLI to retrieve PRISM data history at a point",
    author = "Travis Williams",
    author_email = "travis.williams@colorado.edu",
    
    install_requires = ['netCDF4', 'numpy', 'pandas', 'xarray']
    )