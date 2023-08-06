import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing :: Markup",
]

LICENSE = "MIT"
PLATFORMS = "Any"
setuptools.setup(
    name='vegetablesclassify',
    version='0.0.8',
    author='chengzi',
    author_email='18730850852@163.com',
    description='vegetables classify',
    long_description=long_description,
    url='https://github.com/juebanchengzi/vegetablesclassify',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    license=LICENSE,
    platforms=PLATFORMS,
 )
