from setuptools import setup, find_packages

__VERSION__ = '0.0.1'

setup(
    name='rsnsfw',
    version=__VERSION__,
    description="Reckonsys NSFW fork",  # NOQA
    long_description="NSFW detection",
    url='https://github.com/reckonsys/rsnsfw',
    author='rockyzhengwu',
    author_email='zhengwu@midday.me',
    maintainer='reckonsys',
    maintainer_email='info@reckonsys.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='reckonsys nsfw',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
    ],
)
