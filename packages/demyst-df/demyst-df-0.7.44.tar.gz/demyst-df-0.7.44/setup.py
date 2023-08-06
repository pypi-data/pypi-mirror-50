from setuptools import setup


setup(
    name='demyst-df',

    version='0.7.44',

    description='',
    long_description='',

    author='Demyst Data',
    author_email='info@demystdata.com',

    license='',
    entry_points='''
        [console_scripts]
        demyst-data-function=demyst.df.command:cli
    ''',
    packages=['demyst.df'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'demyst-common>=0.7.44',
        'click',
        'boto3',
        'botocore',
        'tabulate',
        'halo',
        'glom'
    ]
)
