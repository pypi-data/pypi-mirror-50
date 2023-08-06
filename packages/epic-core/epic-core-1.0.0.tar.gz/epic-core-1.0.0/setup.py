import os
from setuptools import find_packages, setup
import epic_core

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name= epic_core.__name__,
    version= epic_core.__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Custom django admin core module',
    long_description=README,
    url='https://github.com/sasri-djproject/epic_core',
    author=epic_core.__author__,
    author_email='sasri.djproject@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires = [
        'django',
        ]
)
