from setuptools import setup


setup(name='cli_tool_test',
      version='0.0.1',
      description='Sample CLI tool in python',
      packages=['cli_tool_test'],
      install_requires=[
          'numpy',
      ],
      zip_safe=True,
      include_package_data=True
      )
