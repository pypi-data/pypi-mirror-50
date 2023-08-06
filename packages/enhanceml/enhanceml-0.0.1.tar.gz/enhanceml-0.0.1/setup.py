import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


#Packages to be installed
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()
		
		
setuptools.setup(
    name="enhanceml",
    version="0.0.1",
    author="Sumit Chandak",
    author_email="chandaksumit29@gmail.com",
    description="An ML enhancement package to improve outcomes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
	url="https://github.com/sumitc29/enhanceml.git",
    
	packages=['enhanceml'],
	license= 'MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	zip_safe=False)