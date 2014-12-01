from setuptools import setup, find_packages

setup(
    version='v0.0.1',
    description='django-shotgun-tools',
    long_description=open('README.md').read(),
    author='Cluster Studio',
    author_email='soporte@clusterstudio.com',
    name='shotgun_tools',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'shotgun_api3',
        'ShotgunORM',
        'django-tastypie',
        'django>=1.7.1'
    ],
    license="MIT",
)
