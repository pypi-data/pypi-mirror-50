from setuptools import setup

setup(
    name='howcode',
    version="0.1.1",
    description='Instant Cross Platform coding answers via the command line',
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
    keywords='howdoi help console command line answer termux',
    author='Val (zvtyrdt.id)',
    author_email='alviandtm@gmail.com',
    url='https://github.com/zevtyardt',
    license='MIT',
    py_modules=["howcode"],
    entry_points={
        'console_scripts': [
            'howcode = howcode:cli',
        ]
    },
    install_requires=[
        'requests',
        'cachelib',
        'bs4',
        'pygments'
     ]
)
