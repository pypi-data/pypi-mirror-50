from distutils.core import setup
setup(
  name = 'pynearmap',
  packages = ['pynearmap'],
  version = '0.1.1',
  license='MIT',
  description = 'Lightweight Nearmap API client implemented in pure Python. Read the API documentation at https://docs.nearmap.com/',
  author = 'Sam Ngu',
  author_email = 'sam.ngu@yandex.com',
  url = 'https://github.com/sam-ngu/pynearmap',
  download_url = 'https://github.com/sam-ngu/pynearmap/archive/v0.1.1.tar.gz',
  keywords = ['nearmap', 'api-client'],
  install_requires=[
          'Pillow',
          'python-dotenv',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)