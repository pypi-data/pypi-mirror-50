from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='wat-cli',
    author='Philipp Hack',
    author_email='philipp.hack@gmail.com',
    url='http://github.com/phha/wat',
    version='0.1.0',
    license='MIT',
    description='Get short answers from Wolfram Alpha.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    py_modules=['wat'],
    install_requires=[
        'click',
        'click-config-file',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        wat=wat:wat
    ''',
)
