from distutils.core import setup

setup(
  name = 'percipher',
  packages = ["percipher"],
  version = '1.1',
  license='Apache 2.0',
  description = 'Simple cipher with permutation',
 # long_description=open('README.md','rt').read(),
  #long_description_content_type='text/markdown',
  author = 'NonSense',
  author_email = 'valerastatilko@gmail.com',
  url = 'https://github.com/NotStatilko/Permutation.Cipher',
  download_url = 'https://github.com/NotStatilko/Permutation.Cipher/archive/1.1.tar.gz',
  keywords = ['Python', 'Cipher'],

  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Security :: Cryptography',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ]
)
