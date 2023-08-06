from setuptools import setup

setup(name='bond-home',
      version='0.0.3',
      description='Python library for controlling BOND Home Hub',
      long_description_content_type="text/markdown",
      url='http://github.com/nguyer/bond-home',
      author='Nicko Guyer',
      author_email='nguyer@gmail.com',
      license='MIT',
      packages=['bond'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
