from setuptools import setup, find_packages
setup(name='xgram',
      version='0.1.1',
      description='The telegram api',
      long_description='The telegram python api',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='telegram tg tlg subject',
      author='xtery',
      author_email='0x.xtery@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      url='https://github.com/xtery/xgram',
      install_requires=['colorama','requests==2.22.0'])

print('ok')
