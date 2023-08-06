import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='hellodoycode',
      version='0.0.1',
      author='Dong',
      author_email='dongyuncheng1991@gmail.com',
      description='The first installation of python.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='',
      #packages=['helloworld']
      packages=setuptools.find_packages(),
      classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
              ]
#      license='MIT',
#      zip_safe=False
)