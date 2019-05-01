from distutils.core import setup

setup(
    name='AdvancedQuery',
    version='0.1.0',
    author='Omkar Deshpande',
    author_email='deshpandeomkar@gmail.com',
    packages=['advancedquery'],
    scripts=['bin/execute.py'],
    url='http://pypi.python.org/pypi/AdvancedQuery/',
    license='LICENSE.txt',
    description='Advaned query using knowledge graphs for structured documents.',
    long_description=open('README.txt').read(),
    install_requires=[
        'mysql-connector-python',
        'spacy',
        'neo4j'
    ],
)