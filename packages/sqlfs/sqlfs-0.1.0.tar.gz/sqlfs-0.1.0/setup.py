from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sqlfs',
    description='SQLite FUSE filesystem',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.1.0',
    platforms='any',
    author='Alexey Moroz',
    author_email='me@mystex.me',
    url='https://pypi.org/project/sqlfs/',
    license='MIT',
    py_modules=['sqlfs'],
    entry_points={
        'console_scripts': [
            'sqlfs = sqlfs:main',
        ],
    },
    install_requires=['fusepy>=3.0.1', 'tzlocal>=1.5.1'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Filesystems",
    ],
)
