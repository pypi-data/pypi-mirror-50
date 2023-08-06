import os
from setuptools import setup, find_packages

setup(
    name='treepy',
    version="0.1",
    packages=find_packages(),
    author_email = 'kiefl.evan@gmail.com',
    author = 'Evan Kiefl',
    url = 'https://github.com/ekiefl/treepy',
    install_requires=open('requirements.txt','r').readlines(),
    scripts = [os.path.join('bin', 'treepy'),
               os.path.join('bin', 'treepy_python')],
)
