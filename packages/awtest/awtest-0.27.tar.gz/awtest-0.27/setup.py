from setuptools import setup
import setuptools

setup(name='awtest',
      version='0.27',
      description='Bridging gaps between other machine learning and deep learning tools and making robust, post-mortem analysis possible.',
      url='http://github.com/awhedon/gaplearn',
      author='Alexander Whedon',
      author_email='alexander.whedon@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires = [
          'pandas',
          'numpy',
          'sklearn',
          'eli5'
      ],
      zip_safe=False)