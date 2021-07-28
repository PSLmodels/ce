from distutils.core import setup

setup(name='cesurvey',
      version='0.1',
      py_modules=['cesurvey'],
      install_requires=[
          'requests',
          'pandas',
          'numpy',
          'openpyxl'
      ],
)
