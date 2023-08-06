from setuptools import setup

setup(name='bradk',
      version='0.1',
      description='The bradk packages developed by Brad Kim',
      url='http://github.com/bomsoo-kim/packages',
      author='Brad Kim',
      author_email='bk2717@columbia.edu',
      license='MIT',
      packages=['bradk', 'bradk.model_selection', 'bradk.finance', 'bradk.neural_networks'],
      zip_safe=False)