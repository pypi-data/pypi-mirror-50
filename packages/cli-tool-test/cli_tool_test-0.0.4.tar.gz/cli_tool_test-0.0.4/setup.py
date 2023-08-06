from setuptools import setup, find_packages


setup(name='cli_tool_test',
      version='0.0.4',
      description='Sample CLI tool in python',
      packages=find_packages(),
        # py_modules=['prog'],
      install_requires=[
          'Click',
          'pyfiglet'
      ],
        entry_points='''
            [console_scripts]
            greet=cli_tool_test.prog:greet
            generate_ascii_art=cli_tool_test.prog:generate_ascii_art
        ''',
      zip_safe=True,
      include_package_data=True
      )
