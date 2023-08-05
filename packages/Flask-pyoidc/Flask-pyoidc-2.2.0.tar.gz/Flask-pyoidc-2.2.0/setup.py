from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Flask-pyoidc',
    version='2.2.0',
    packages=['flask_pyoidc'],
    package_dir={'': 'src'},
    url='https://github.com/zamzterz/flask-pyoidc',
    license='Apache 2.0',
    author='Samuel Gulliksson',
    author_email='samuel.gulliksson@gmail.com',
    description='Flask extension for OpenID Connect authentication.',
    install_requires=[
        'oic==0.12',
        'Flask',
        'requests'
    ],
    package_data={'flask_pyoidc': ['files/parse_fragment.html']},
    long_description=long_description,
    long_description_content_type='text/markdown',
)
