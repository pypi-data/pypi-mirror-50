import setuptools

#import speak

with open("README.md", "r") as fh:
    long_description = fh.read()
	
setuptools.setup(
     name='speakme',  
     version='0.1.1',
     scripts=['speakme'] ,
     author="Tejas Bhor",
     author_email="tejasjbhor@gmail.com",
     description="Personal voice assistant - Markos",
     long_description=long_description,
	 long_description_content_type="text/markdown",
     url="https://github.com/tejasjbhor/NLP",
     #packages=['speak', ],
	 include_package_data=True,
     classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
 )