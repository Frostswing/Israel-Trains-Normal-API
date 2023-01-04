from setuptools import setup

setup(
    name='israeltrainapi',
    version='1.0.0',
    description='An API for accessing information about trains in Israel',
    author='Eden Aharon',
    author_email='eden.ah.work@gmail.com',
    url='https://github.com/Frostswing/Israel-Trains-Normal-API',
    py_modules=['israeltrainapi'],
    install_requires=[
        'requests',
    ],
)
