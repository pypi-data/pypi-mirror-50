# from setuptools import find_packages, setup
# import sys
# import pprint
# pprint.pprint(sys.path)
# from package import Package
#
# setup(
#     author="Ami Mahloof",
#     author_email="author@email.com",
#     packages=find_packages(),
#     include_package_data=True,
#     cmdclass={
#         "package": Package
#     }
# )

from setuptools import setup

setup(
    name='frameworkaudit',      # name of PyPI package
    version='0.1',          # version number, update with new releases
    packages=['Audit'] # names of packages directories
)