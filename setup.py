from setuptools import setup, find_packages
import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    sys.exit('Sorry, Python < 3.5 is not supported')

setup(name='mrot',
      version='0.4',
      description='Movie ratings over time',
      author='Arthur Brenaut',
      author_email='arthur.brenaut@gmail.com',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['mrot=mrot.cli:main'],
      },
      install_requires=[
          'matplotlib',  # Plotting module
          'bs4',  # BeautifulSoup scraping module
          'Pillow',  # Image library used to display movie posters
          'waybackscraper'
      ],
      zip_safe=False)
