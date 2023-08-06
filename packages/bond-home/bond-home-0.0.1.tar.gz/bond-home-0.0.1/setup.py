from setuptools import setup

setup(name='bond-home',
      version='0.0.1',
      description='Python library for controlling BOND Home Hub',
      url='http://github.com/nguyer/bond-home',
      author='Nicko Guyer',
      author_email='nguyer@gmail.com',
      license='MIT',
      packages=['bond'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
