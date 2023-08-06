from setuptools import setup

setup(name='lyft_av_loo',
      version='0.5',
      description='AV learning on the loo',
      url='https://github.com/lyft/avsoftware',
      author='Jerry Yang, Shawn Liu',
      author_email='av-scenarios@lyft.com',
      license='MIT',
      packages=['lyft_av_loo'],
      include_package_data=True,
      package_data = {
        '': ['*.txt'],
      },
      zip_safe=False)
