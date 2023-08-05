import setuptools

setuptools.setup(
	name="TPM-Service",
	version="1.0.0",
	author="wenzt2",
	author_email="wenzt2@lenovo.com",
	description="Provide restful api service for TPM",
	packages=setuptools.find_packages(),
	platforms='linux',
	install_requires=[
		'Flask==1.1.1',
		'Flask-RESTful==0.3.7',
		'Flask-SQLAlchemy==2.4.0',
		'Flask-Login==0.4.1',
		'passlib==1.7.1',
	],
	classifiers=[
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
	],
)
