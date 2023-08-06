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
     name='servicesframework',
     version='0.1',
     packages=['Audit'] ,
     author="Akhilesh",
     author_email="kafkaservices@gmail.com",
     description="A Docker and AWS utility package",
     long_description="kafka",
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     # packages=setup().find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )