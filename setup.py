from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='genetic_optimizer',
      version='1.0',
      description='...',
      long_description=readme(),
      classifiers=[
        'Development Status :: Active',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
#        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='...',
      url='https://github.com/szachovy/GeneticOptimizer',
      author='WJ Maj',
      license='MIT',
      packages=['genetic_optimizer'],
      install_requires=[
          '...',
      ],
#      test_suite='nose.collector',
#      tests_require=['nose', 'nose-cover3'],
      entry_points={
#          'console_scripts': ['funniest-joke=funniest.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
