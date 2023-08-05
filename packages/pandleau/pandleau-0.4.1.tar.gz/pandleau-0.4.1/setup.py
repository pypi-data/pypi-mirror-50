from setuptools import setup, find_packages


setup(name='pandleau',
      version='0.4.1',
      packages=find_packages(exclude=['tests*']),
      license='MIT',
      description='A quick and easy way to convert a Pandas DataFrame to a Tableau extract.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      install_requires=['pandas', 'numpy', 'tqdm'],
      author='Benjamin Wiley, Zhirui(Jerry) Wang, Aaron Wiegel, Pointy Shiny Burning, Harrison',
      author_email = 'bewi7122@colorado.edu, zw2389@columbia.edu, aawiegel@gmail.com',
      url='https://github.com/bwiley1/pandleau',
      download_url='https://github.com/bwiley1/pandleau/dist/pandleau-0.4.1.tar.gz',
      py_modules=['pandleau'],
      keywords='tableau pandas extract tde hyper',
      classifiers=['Programming Language :: Python'])
