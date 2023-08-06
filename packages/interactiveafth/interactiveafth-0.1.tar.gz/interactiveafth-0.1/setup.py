from distutils.core import setup
setup(
  name = 'interactiveafth',
  packages = ['interactiveafth'],
  version = '0.1',
  license='MIT',
  description = 'Interactive environment within Py-EVM for ActorForth Programming language',
  author = 'Viacheslav Litvinov',
  author_email = 'viacheslavlitvinov@gmail.com',
  url = 'https://github.com/TheLitvinoff/interactiveafth',
  download_url = 'https://github.com/TheLitvinoff/interactiveafth/archive/0.1.tar.gz',    # I explain this later on
  keywords = [],
  install_requires=[
        "eth-utils>=1,<2",
        "py-evm", 
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)