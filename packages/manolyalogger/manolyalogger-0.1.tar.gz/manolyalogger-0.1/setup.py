from setuptools import setup, find_packages

setup(name='manolyalogger',
      version='0.1',
      description='The simplest logger the world',
      long_description='Really, the simplest around.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='simplest logger',
      url='http://github.com/storborg/funniest',
      author='Umut Ucok',
      author_email='ucok.umut@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)