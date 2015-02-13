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
    dependency_links=[
        "https://github.com/shotgunsoftware/python-api/tarball/master#egg=shotgun_api3",
        "https://github.com/ClusterStudio/python-shotgunorm/tarball/lazy_results#egg=ShotgunORM"
    ],
    install_requires=[
        'shotgun_api3',
        'ShotgunORM',
        'django-tastypie',
        'django>=1.7.1'
    ],
    license="MIT",
)
