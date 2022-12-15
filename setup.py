import setuptools
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name = 'xfftspy',
    version = "0.1.3",
    description = '',
    long_description = long_description,
    long_description_content_type = "text/markdown",
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
