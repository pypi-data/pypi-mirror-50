from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='pdpm',
    version='0.1',
    url='https://github.com/Okirshen/pdpm',
    license='MIT',
    author='Ofri Kirshen',
    author_email='okirshen@gmail.com',
    description='Python project manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pdpm=pdpm:cli
    ''',
)
