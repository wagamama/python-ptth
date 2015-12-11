from setuptools import setup


setup(name = 'ptth',
      version = '0.1',
      description = 'Reverse HTTP (PTTH) for Python',
      keywords = 'ptth reverse http',
      url = 'https://github.com/wagamama/python-ptth',
      author = 'Yi-Lung (Bruce) Tsai',
      author_email = 'wagamama.tsai@gmail.com',
      license = 'Apache',
      packages = ['ptth'],
      test_suite = 'nose.collector',
      tests_require = ['nose']
)
