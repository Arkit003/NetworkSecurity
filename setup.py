from setuptools import find_packages,setup
from typing import List


HYPEN_E_DOT="-e ."


def get_requirements()->List[str]:
    '''
    This returns the list of requirements
    '''
    try:
        with open('requirements.txt','r') as file_obj:
            requirements=file_obj.readlines()
            requirements=[req.strip() for req in requirements]
            
            

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
        


    except FileNotFoundError:
        return []
        
    return requirements

setup(
    name="Network Security",
    version='0.0.1',
    author='Arkit',
    author_email='arkit312005@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)
    
