import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hgfinance',
    version='0.0.1',
    author='José Almir',
    author_email='resilientcod@gmail.com',
    license='MIT',
    description='Um pacote que facilita o acesso à API HG finance.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/resilientcod/hgfinance-python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese (Brazilian)'
    ],
    keywords='api hgfinance currency quotation selic cdi dollar hgbrasil'
)
