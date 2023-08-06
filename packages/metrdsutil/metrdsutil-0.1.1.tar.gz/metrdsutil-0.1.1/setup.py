from distutils.core import setup
setup(
  name = 'metrdsutil',         # How you named your package folder (MyLib)
  packages = ['metrdsutil'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Common exploratory data functionality for METR',   # Give a short description about your library
  author = 'Daniel Hopp',                   # Type in your name
  author_email = 'daniel.hopp@metr.systems',      # Type in your E-Mail
  url = 'https://bitbucket.org/danielhopp/metrdsutil/',   # Provide either the link to your github or to your website
  download_url = 'https://bitbucket.org/danielhopp/metrdsutil/get/v0.1.1.tar.gz',    # I explain this later on
  keywords = ['data science', 'exploratory analysis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support
  ],
)
