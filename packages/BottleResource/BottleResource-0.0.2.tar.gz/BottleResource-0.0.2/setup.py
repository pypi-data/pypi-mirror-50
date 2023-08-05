import os

from setuptools import setup


def read_file(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8') as c:
            return c.read()
    except Exception as e:
        return None


setup(
    name='BottleResource',
    version='0.0.2',
    packages=['.'],
    url='https://github.com/theo-l/bottle-resource',
    license='',
    author='Liang Guisheng',
    author_email='theol.liang@foxmail.com',
    description='Class based bottle endpoint resource plugin',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    include_package_data=True
)
