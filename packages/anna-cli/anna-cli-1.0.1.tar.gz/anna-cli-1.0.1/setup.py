import setuptools

with open('README.md', 'r') as f:
	description = f.read()

setuptools.setup(
	name='anna-cli',
	version='1.0.1',
	author='Patrik Pihlstrom',
	author_email='patrik.pihlstrom@gmail.com',
	url='https://github.com/patrikpihlstrom/anna-cli',
	description='cli for anna',
	long_description=description,
	long_description_content_type='text/markdown',
	packages=['anna_cli'],
	entry_points={'anna': ['anna_cli = anna_cli.__main__:main']},
	install_requires=[
		'click',
		'anna-client'
	]
)
