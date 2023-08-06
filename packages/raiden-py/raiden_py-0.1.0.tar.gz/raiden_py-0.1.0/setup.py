import pathlib
from setuptools import setup

PARENT_DIR = pathlib.Path(__file__).parent
README = (PARENT_DIR / "README.md").read_text()

setup(
    name='raiden_py',
    version='0.1.0',
    packages=['raiden_py'],
    include_package_data=True,
    url='https://github.com/viraja1/raiden_py/',
    license='MIT',
    author='viraj',
    author_email='',
    description='Raiden Python Client Library',
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=[
       'requests>=2.22.0'
    ],
    keywords="raiden",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7"
)
