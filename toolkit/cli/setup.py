from setuptools import setup, find_packages

setup(
    name='gitflow-cli',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['cli'],
    install_requires=[
        'click',
        'PyGithub',
        'rich',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'gitflow-cli=cli:cli',
        ],
    },
)
