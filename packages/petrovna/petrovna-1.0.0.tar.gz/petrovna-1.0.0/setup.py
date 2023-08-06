from setuptools import setup, find_packages



setup(
    name='petrovna',
    version='1.0.0',
    description='Validatee bic, inn, kpp, ogrn, ogrnip, corr. account, account number, snils',
    url='https://example.com',
    author='KODE LLC',
    platforms='Any',
    packages=find_packages(exclude=('tests',)),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    zip_safe=False
)
