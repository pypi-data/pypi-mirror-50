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
# from bin.core.applications.AuditManagement
# from bin.core.applications.AuditManagement import Audit
# UserManagementACStrategies.generate_audit_data("jdfnd","jdbjd","jhj","jj")
import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
setuptools.setup(
    name='sunday_12',
    version='0.1',
    packages=['Audit'],
    author="Akhilesh",
    setup_requires=['wheel'],
    author_email="kafkaservice@gmail.com",
    description="A Docker and AWS utility package",
    long_description="Long desc",
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

 )