from setuptools import setup

setup(
    install_requires=[
        'requests',
    ],
    name='pyvotal_tracker',
    version='0.0.1',
    description='Pivotal Tracker API module',
    author='Alireza Tajik',
    author_email='alireza7192@gmail.com',
    license='MIT',
    packages=['pyvotal_tracker', ],
    zip_safe=False
)
