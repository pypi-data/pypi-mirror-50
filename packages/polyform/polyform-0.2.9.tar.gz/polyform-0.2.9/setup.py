import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name='polyform',
    version = "0.2.9",
    packages=['polyform'],
    license='None',
    description = 'Serverless DataOps, for AI/ML purposes (Prototype)',
    long_description=open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author = 'Brandon Gillespie',
    author_email = 'bjg-pypi@cold.org',
    url = 'https://github.com/srevenant/polyform',
    keywords = [ 'dictlib', 'pyyaml', 'pylint', 'pyjwt', 'boto3', 'graphql' ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
