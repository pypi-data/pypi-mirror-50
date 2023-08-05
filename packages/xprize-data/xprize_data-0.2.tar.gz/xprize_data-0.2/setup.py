from setuptools import setup

setup(name='xprize_data',
      version='0.2',
      description='Xprize Data Commons',
      url='https://github.com/xprizewebadmin/Data-Commons',
      author='Max Cappellari',
      author_email='max@xprize.org',
      license='MIT',
      packages=['xprize_data'],
      zip_safe=False,
      install_requires = [
          'azure-storage',
          'pyarrow',
          'pandas',
          'ipywidgets'] )
