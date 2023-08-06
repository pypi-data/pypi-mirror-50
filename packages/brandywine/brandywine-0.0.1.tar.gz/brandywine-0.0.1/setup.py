import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="brandywine",
	version="0.0.1",
	author="Florian Matter",
	author_email="florianmatter@gmail.com",
	description="A simple pomodoro timer",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/florianmatter/brandywine",
	packages=setuptools.find_packages(),
	entry_points={
		"console_scripts": ["brandywine = brandywine.command_line:main"],
	},
	classifiers=[
        	"Programming Language :: Python :: 3",
        	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        	"Operating System :: OS Independent",
    	]
)
