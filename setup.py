import setuptools

setuptools.setup(
    name = 'xfftspy',
    version = __import__('xfftspy').__version__,
    description = '',
    url = 'https://github.com/ogawa-ros/xfftspy',
    author = 'Nishimura, Atsushi',
    author_email = 'ars096@gmail.com',
    license = 'MIT',
    keywords = '',
    packages = [
        'xfftspy',
    ],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
