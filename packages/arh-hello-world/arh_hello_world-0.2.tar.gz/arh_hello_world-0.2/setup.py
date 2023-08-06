from distutils.core import setup

setup(
    name='arh_hello_world',
    packages=['arh_hello_world'],
    version='0.2',
    license='MIT',
    description='My first pype project upload',
    author='Alencar Rodrigo Hentges',
    author_email='alencarhentges@gmail.com',
    url='https://github.com/alencarrh/',
    download_url='https://github.com/alencarrh',
    keywords=['MY', 'FIRST', 'PROJECT', 'TO', 'PYPI', "UPLOAD"],
    install_requires=[

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
