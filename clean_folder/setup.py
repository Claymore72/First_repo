from setuptools import setup, find_packages

setup(
    name='clean-folder',
    version='0.0.1',
    packages=find_packages(),
    author = 'Claymore',
    description=' Clean folder from trash',
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main',
        ],
    },
)
