import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='poise-cli',
    version='1.0',
    scripts=['poise'] ,
    author='Abdullah Alharbi',
    author_email='user.afh@gmail.com',
    description='Poise, a CLI for retrieving quotes on Goodreads',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/harbi/poise',
    packages=setuptools.find_packages(),
    install_requires=[
        'scrapy',
        'click',
        'langdetect',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
