from distutils.core import setup
setup(
  name = 'potentialfinder',         # How you named your package folder (MyLib)
  packages = ['potentialfinder'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Finding high-potential patterns in your data',   # Give a short description about your library
  author = 'Mathias Riechert',                   # Type in your name
  author_email = 'mathias.riechert@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/patternsearch/potentialfinder',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/patternsearch/potentialfinder/archive/v_07.tar.gz',    # I explain this later on
  keywords = ['pattern search', 'python', 'exponential patterns'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
		  'scipy',
		  'matplotlib',
		  'numpy',
		  'python-dateutil',
		  
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)



