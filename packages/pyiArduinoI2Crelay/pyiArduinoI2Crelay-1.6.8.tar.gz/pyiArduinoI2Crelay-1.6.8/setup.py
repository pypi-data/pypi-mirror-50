from distutils.core import setup
from distutils.extension import Extension

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(name='pyiArduinoI2Crelay',
    version='1.6.8',
    description='iarduino.ru module for Raspberry Pi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='http://github.com/tremaru/pyiArduinoI2Crelay',
    author='iarduino.ru',
    author_email='shop@iarduino.ru',
    license='MIT',
    package=['pyiArduinoI2Crelay'],
    ext_modules = [Extension(
        name="pyiArduinoI2Crelay",
        sources=["pyiArduinoI2Crelay/pyiArduinoI2Crelay.cpp"])],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
)
