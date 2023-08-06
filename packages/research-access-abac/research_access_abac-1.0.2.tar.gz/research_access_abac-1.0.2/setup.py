from setuptools import setup, find_packages


def extract_requirements(req):
	return req.split("\n")[:-1]  


reqs = extract_requirements(open("requirements.txt", "r").read())
print("Req: {}".format(reqs))

setup(
	name="research_access_abac",
	version="1.0.2",
	description="Implementation of ABAC for research data files",
	long_description=open("README.md", "r").read(),
	packages=find_packages(),
	include_package_data=True,
	install_requires=extract_requirements(open("requirements.txt", "r").read()),
	author="Catherine Nyambura, Eddy Mwenda",
)
