from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='BuyProxiesAPI',
    version='0.21',
    description='BuyProxies.org simple API Wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Druidmaciek/BuyProxies.org-API-Wrapper',
    download_url='https://github.com/Druidmaciek/BuyProxies.org-API-Wrapper/archive/0.21.tar.gz',
    author='Maciej Janowski',
    author_email='maciekjanowski@icloud.com',
    packages=['buyproxies_api'],
    include_package_data=True,
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='web proxies development scraping buyproxies.org',
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/Druidmaciek/BuyProxies.org-API-Wrapper/issues',
        'Funding': 'https://paypal.me/druidmaciek',
        'Source': 'https://github.com/Druidmaciek/BuyProxies.org-API-Wrapper'
    },
)

__author__ = "Maciej Janowski"
