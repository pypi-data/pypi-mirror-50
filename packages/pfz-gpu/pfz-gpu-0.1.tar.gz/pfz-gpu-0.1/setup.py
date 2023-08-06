from setuptools import setup


requirements = ['hpccm']

setup(
    # metadata
    name='pfz-gpu',
    version='0.1',
    author='Stephen Ra',
    author_email='stephen.ra@pfizer.com',
    url='https://github.com/PfizerRD/gpu',
    descrption='GPU utilities for accelerated computing at Pfizer',
    install_requires=requirements,
    license='MIT',
    zip_safe=True
)
