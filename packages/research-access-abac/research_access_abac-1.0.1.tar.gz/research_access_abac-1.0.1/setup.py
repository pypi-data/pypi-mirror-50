from setuptools import setup, find_packages


def extract_requirements(req):
	return req.split("\n")[:-1]  


setup(
	name="research_access_abac",
	version="1.0.1",
	description="Implementation of ABAC for research data files",
	long_description=open("README.md", "r").read(),
	packages=find_packages(),
	include_packages=True,
	requirements=extract_requirements(open("requirements.txt", "r").read()),
	author="Catherine Nyambura",
)

