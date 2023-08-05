from distutils.core import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='selenium_testing_module',
    packages=['selenium_testing_module'],
    version='1.0.2',
    license='MIT',
    description='This is a module which can be used with Selenium to make testing scripts easier to read and write. The module automates some hectic parts of testing such as browser initiation and styles command line output for better, more understandable test results.',
    author='Navaz Alani',
    author_email='nalani@uwaterloo.ca',
    url='https://github.com/navaz-alani/selenium-testing-module/',
    download_url='https://github.com/navaz-alani/selenium-testing-module/archive/v1.0.2Beta.tar.gz',
    keywords=[
        'testing',
        'selenium',
        'webdriver',
        'automation'
    ],
    install_requires=[
        'selenium',
        'webdrivermanager',
        'colorama'
    ],
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
