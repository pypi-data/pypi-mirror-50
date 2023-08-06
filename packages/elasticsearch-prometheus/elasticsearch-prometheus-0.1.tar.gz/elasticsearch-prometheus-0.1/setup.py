from distutils.core import setup

setup(
    name='elasticsearch-prometheus',
    version='0.1',
    packages=['elasticsearch-prometheus',],
    license='apache2',
    long_description=open('README').read(),
    install_requires=[
        'elasticsearch>=7.0.0,<8.0.0',
        'prometheus-client>=0.7,<0.8'
    ],
    url='https://github.com/wesparish/elasticsearch-prometheus',
    author='Wes Parish',
    author_email='wes@elastiscale.net',
)
