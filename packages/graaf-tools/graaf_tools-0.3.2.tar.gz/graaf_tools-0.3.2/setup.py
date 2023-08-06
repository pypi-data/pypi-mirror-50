from distutils.core import setup
setup(
  name = 'graaf_tools',
  packages = ['graaf_tools'],
  version = '0.3.2',
  license='MIT',
  description = 'tools and code for research',
  author = 'Rafael Van Belle',
  author_email = 'rafael.vanbelle@gmail.com',
  url = 'https://github.com/raftie/graaf_tools',
  download_url = 'https://github.com/Raftie/graaf_tools/archive/v0.3.2.tar.gz',
  keywords = ['network'],
  install_requires=[
          'tqdm',
          'gensim',
          'networkx',
      ],
  classifiers=[
  ],
)
