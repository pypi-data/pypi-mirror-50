import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='espapp_pkg',
      version='0.3',
      description='ESP applicaion',
      author='Karan',
      author_email='karan.rathore@viriminfotech.com',
      license='Virim',
      url = "https://github.com/emb-karan/espapp",
      packages=setuptools.find_packages(),
      install_requires=[
          'uuid',
          'python-crontab',
          'requests',
      ],
      entry_points={  # Optional
        'console_scripts': [
            'espapp=espapp:main',
        ],
       },
      )
      
