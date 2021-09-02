from distutils.core import setup

setup(name='cesurvey',
      packages=['cesurvey'],
      version='0.1.1',
      license='GPLv3',
      description='Utilities for the Consumer Experience Survey',
      url='https://github.com/PSLmodels/cesurvey'
      install_requires=[
          'requests',
          'pandas',
          'numpy',
          'openpyxl'
      ],
)
