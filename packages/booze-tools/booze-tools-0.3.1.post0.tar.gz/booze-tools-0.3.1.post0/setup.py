import setuptools

setuptools.setup(
	name='booze-tools',
	version='0.3.1.post0',
	packages=[
		'boozetools',
		'boozetools.macroparse',
		'boozetools.parsing',
		'boozetools.scanning',
		'boozetools.support',
	],
	description='A panoply of tools for parsing and lexical analysis',
	long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
	url="https://github.com/kjosib/booze-tools",
	classifiers=[
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: Compilers",
		"Development Status :: 4 - Beta",
    ],
)