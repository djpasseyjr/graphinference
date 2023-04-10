import setuptools 

setuptools.setup(name='graphinference',
      version='0.1',
      description='Network inference from timeseries data',
      url='',
      author='DJ Passey',
      author_email='djpasseyjr@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=['numpy'],
      setup_requires=['wheel'],
      zip_safe=False)