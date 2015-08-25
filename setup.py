from distutils.core import setup

VERSION = open('VERSION', 'r').read().strip()

setup(name='gt',
      version=VERSION,
      description='Google Translate library and clients',
      long_description='''\
Includes a library for Google Translate (gt), a console client (gt_console), an
xsel+libnotify client (gt_notify) and some other utilites.''',
      author='shdown',
      author_email='shdownnine@gmail.com',
      url='https://github.com/shdown/gt',
      download_url='https://github.com/shdown/gt/tarball/' + VERSION,
      license='LGPLv3',
      packages=['gt'],
      scripts=['gt_console', 'gt_notify', 'gt_dump_json', 'gt_play',
               'gt_languages'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Topic :: Internet',
          'Topic :: Utilities',
      ],
     )
