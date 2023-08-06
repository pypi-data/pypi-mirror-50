import setuptools

with open('README.md', 'r') as f:
	description = f.read()

setuptools.setup(
	name='anna-dashboard',
	version='0.0.1',
	author='Patrik Pihlstrom',
	author_email='patrik.pihlstrom@gmail.com',
	url='https://github.com/patrikpihlstrom/anna-dashboard',
	description='anna dashboard',
	long_decription=description,
	long_description_content_type='text/markdown',
	packages=['dashboard', 'dashboard.jobs', 'dashboard.unittests', 'dashboard.jobs.migrations', 'dashboard.unittests.migrations']
)
