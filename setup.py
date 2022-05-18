from setuptools import setup, find_namespace_packages

from os.path import join, dirname, realpath, isfile

requirements_path = join(dirname(realpath(__file__)), "requirements.txt")
install_requires = list()
if isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

setup(
    name='personal_assistant_cli',
    version='1.0',
    description='A personal assistant that will make your life easier and \
help you unleash your creative potential. Join your inspired! Leave the \
routine to our assistant!',
    url='https://github.com/vita-olshevska/personal_assistant_cli/',
    author='SpaceV',
    author_email='vaolshevska@gmail.com',
    maintainer='http://140.238.212.157/index.html',
    license='GNU General Public License',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['personal_assistant_cli = personal_assistant_cli.main:main']},
    install_requires=install_requires
)
