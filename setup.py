from setuptools import setup, find_packages

setup(name='mrot',
      version='0.1',
      description='Movie ratings over time',
      author='Arthur Brenaut',
      author_email='arthur.brenaut@gmail.com',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['mrot=mrot.mrot:main'],
      },
      install_requires=[
          'matplotlib',  # Plotting module
          'bs4',  # BeautifulSoup scraping module
          'Pillow'  # Image library used to display movie posters
      ],
      zip_safe=False)
