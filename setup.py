from setuptools import setup, find_packages
from os import path

pwd = lambda f: path.join(path.abspath(path.dirname(__file__)), f)
contents = lambda f: open(pwd(f)).read().strip()

package = 'disposable_consul'

setup(
    name=package,
    version=contents('VERSION'),
    py_modules=[package],
    author='EverythingMe',
    description='''
Disposable Consul - Helper for unit testing with Consul
    '''
)
