from setuptools import setup, find_packages

setup(
    name='arules',
    version='0.1.0',
    description='Apriori algorithm implementation to mine association rules',
    #long_description=open('README.rst').read(),
    author='Ege Can Özer, Agustin Zuñiga',
    #author_email='ege.zer',
    url='https://github.com/HEL-DMP17/Apriori',
    packages=find_packages(exclude=['docs', 'tests', 'know-how']),
    install_requires=[
        'lxml'
    ],
    license="BSD",
    zip_safe=False,
    keywords='arules, apriori',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)