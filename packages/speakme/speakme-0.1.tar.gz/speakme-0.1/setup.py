import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='speakme',  
     version='0.1',
     scripts=['markos'] ,
     author="Tejas Bhor",
     author_email="tejasjbhor@gmail.com",
     description="Speech Assistant",
     long_description="Markos is your personal voice assistant / software agent that can perform tasks or services for an individual based on verbal commands and strong recommandation system which help you in decision making.",
	 long_description_content_type="text/markdown",
     url="https://github.com/tejasjbhor/NLP",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )