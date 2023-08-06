import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='treepy',
    version="0.2",
    description="Bare-bones CLI for displaying a tree of file structure",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    author_email = 'kiefl.evan@gmail.com',
    author = 'Evan Kiefl',
    url = 'https://github.com/ekiefl/treepy',
    install_requires=open('requirements.txt','r').readlines(),
    scripts = [os.path.join('bin', 'treepy'),
               os.path.join('bin', 'treepy_python')],
)
