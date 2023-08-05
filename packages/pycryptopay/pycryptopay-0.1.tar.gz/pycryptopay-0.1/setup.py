from distutils.core import setup

setup(
    name='pycryptopay',
    packages=['cryptopay'],
    version='0.1',
    license='MIT',
    description='Library that helps you to implement CryptoPay API',
    author='CryptoPay',
    author_email='auth@cryptopay.click',
    url='https://github.com/CryptoPayClick/pycryptopay',
    download_url='https://github.com/CryptoPayClick/pycryptopay/archive/v0.1.tar.gz',
    keywords=['crypto', 'cryptocurrency', 'bitcoin', 'eth', 'btc', 'ethereum', 'python'],  # Keywords that define your package best
    install_requires=[
        'aiohttp',
        'asyncio',
        'requests',
        'python-dateutil'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
