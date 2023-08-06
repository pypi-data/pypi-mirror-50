from setuptools import setup, find_namespace_packages

version = "v0.1.9"

setup(
  name = 'metrdsutil',
  packages = find_namespace_packages(),
  version = version,
  license='MIT',
  description = 'Common exploratory data functionality for METR',
  author = 'Daniel Hopp',
  author_email = 'daniel.hopp@metr.systems',
  url = 'https://bitbucket.org/danielhopp/metrdsutil/',
  download_url = f'https://bitbucket.org/danielhopp/metrdsutil/get/{version}.tar.gz',
  keywords = ['data science', 'exploratory analysis'],
  install_requires=[
          'matplotlib',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
