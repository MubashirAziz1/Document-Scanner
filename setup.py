from setuptools import find_packages, setup
import os

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path):
    """Function will return the list of requirements"""
    requirements = []
    if os.path.exists(file_path):
        with open(file_path) as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.replace('\n','') for req in requirements]
            
            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='Document_Scanner',
    version='0.0.1',
    author='Mubashir',
    author_email='cs.mubashir.a@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    python_requires='>=3.7',
)