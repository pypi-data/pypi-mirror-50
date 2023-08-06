from setuptools import setup, find_packages


requirements_file = open("requirements.txt", "r")
# Remove newline characters in the list of requirements
requirements = [requirement.strip() for requirement in \
				requirements_file.readlines()]

setup(
	name="ra_crypto",
	version="1.0.2",
	description="A python module with encryption and decryption\
				algorithms for RSA based IBE and AES",
	packages=find_packages(),
	include_package_data=True,
	long_description=open("README.md", "r").read(),
	install_requires=requirements,
	author="EddyMM",
	author_email="mwendaeddy@gmail.com",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	]
)
