from setuptools import setup

setup(
    name='zerobouncesdk',
    version='0.0.5',
    description='The ZeroBounce SDK for Python programming language',
    license='MIT',
    packages=['zerobouncesdk'],
    author='ZeroBounce',
    author_email='integrations@zerobounce.net',
    keywords=['zero', 'bounce', 'sdk'],
    url='https://github.com/zerobounce-llc/zero-bounce-python-sdk', install_requires=['requests', 'requests_toolbelt']
)
