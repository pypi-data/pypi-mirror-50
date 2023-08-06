from setuptools import setup

setup(
    name='fecho',
    version='1.0.2',
    packages=['fecho'],
    url='https://github.com/thehappydinoa/fecho',
    license='MIT',
    author='thehappydinoa',
    author_email='thehappydinoa@gmail.com',
    description='Requests wrapper that uses Facebook Developer tool echo.',
    entry_points={'console_scripts': ['fecho = fecho.cli:main']},
    install_requires=['requests']
)
