from setuptools import setup

setup(name='python-ltaoist',
      version='0.3',
      description='Let import ltaoist and from ltaoist import start',
      url='http://github.com/dist1/python-ltaoist',
      author='ltaoit',
      author_email='ltaoist6@gmail.com',
      license='GPLv3',
      packages=[
          'ltaoist',
          'ltaoist.beta_machine',
          'ltaoist.plane_calculation'
      ],
      zip_safe=False
)
