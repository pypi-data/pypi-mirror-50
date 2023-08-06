import setuptools
from pathlib import Path

setuptools.setup(
    name="chess-board",
    version="0.1.8",
    author="Ahira Adefokun",
    author_email="justiceahira@gmail.com",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(),
    package_dir={'chessboard': 'chessboard'},
    package_data={'chessboard': ['images/*.png']},
    install_requires=[
        'pygame',
    ],
)