from setuptools import setup

setup(
    name='rgxg',
    version="1.2.2",
    description='ReGular eXpression Generator',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Documentation",
    ],
    keywords='Regular Expression Generator Toolkit',
    author='Val (zvtyrdt.id)',
    author_email='alviandtm@gmail.com',
    url='https://github.com/zevtyardt',
    license='MIT',
    packages=["rgxg"],
    entry_points={
        'console_scripts': [
            'rgxg = rgxg.rgxg:main',
        ]
    },
)
