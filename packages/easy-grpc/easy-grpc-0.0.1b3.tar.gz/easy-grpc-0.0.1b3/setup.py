import setuptools
from distutils.core import setup

requirements = open('requirements.txt').read().split('\n')

setup(
    name='easy-grpc',
    description='Helper module to build GRPC service easily',
    url='https://gitlab.com/ist-supsi/istsosm/utils/easygrpc',
    project_urls={
        'Documentation': 'https://gitlab.com/ist-supsi/istsosm/utils/easygrpc',
        'Source': 'https://gitlab.com/ist-supsi/istsosm/utils/easygrpc',
        'Tracker': 'https://gitlab.com/ist-supsi/istsosm/utils/easygrpc/issues',
    },
    author='IST-SUPSI',
    author_email='geoservice@supsi.ch',
    version='0.0.1b3',
    packages=setuptools.find_packages(),
    install_requires=[x for x in requirements if x],
    python_requires='>=3, <4',
    license='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='istsos grpc',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
