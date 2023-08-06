import ast
import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_webpack_html_helper.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='Oliver Epper',
    author_email='oliver.epper@gmail.com',
    description=description,
    keywords='Lektor plugin webpack html-webpack-plugin',
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-webpack-html-helper',
    packages=find_packages(),
    py_modules=['lektor_webpack_html_helper'],
    url='https://github.com/oliverepper/lektor-webpack-html-helper',
    version='0.1.2',
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
    ],
    entry_points={
        'lektor.plugins': [
            'webpack-html-helper = lektor_webpack_html_helper:WebpackHtmlHelperPlugin',
        ]
    },
    install_requires=['watchdog']
)
