import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='selenium_testing_module',
    packages=setuptools.find_packages(),
    version='1.0.3',
    license='MIT',
    description='A module to be used with Selenium; helps make test scripts easier to write.',
    author='Navaz Alani',
    author_email='nalani@uwaterloo.ca',
    url='https://github.com/navaz-alani/selenium-testing-module/',
    download_url='https://github.com/navaz-alani/selenium-testing-module/archive/v1.0.2Beta.tar.gz',
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    ]
)
