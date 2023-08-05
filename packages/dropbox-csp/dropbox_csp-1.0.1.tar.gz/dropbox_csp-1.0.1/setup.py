from setuptools import setup, find_packages


def extract_requirements(requirements_file):
	requirements = open(requirements_file, "r").read()
	listed_requirements = requirements.split("\n")[:-1]
	return listed_requirements


setup(
	name="dropbox_csp",
	author="EddyMM",
	author_email="mwendaeddy@gmail.com",
	version="1.0.1",
	description="Dropbox wrapper client to upload data files to a folder",
	long_description=open("README.md", "r").read(),
	packages=find_packages(),
	include_package_data=True,
	install_requires=extract_requirements("requirements.txt"),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
