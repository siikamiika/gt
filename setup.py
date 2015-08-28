from distutils.core import setup

# Get the version from gt/version.py without importing the package
exec(compile(open('gt/version.py').read(), 'gt/version.py', 'exec'))

setup(name='gt',
      version=__version__,
      description='Google Translate library and clients',
      long_description='''\
Includes a library for Google Translate (gt), a console client (gt_console), an
xsel+libnotify client (gt_notify) and some other utilites.''',
      author='shdown',
      author_email='shdownnine@gmail.com',
      url='https://github.com/shdown/gt',
      download_url='https://github.com/shdown/gt/tarball/v' + __version__,
      license='LGPLv3',
      packages=['gt'],
      scripts=['gt_console', 'gt_notify', 'gt_dump_json', 'gt_play',
               'gt_languages'],
      platforms=['any'],
      keywords=['gt', 'google', 'translate', 'translation', 'google translate'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Topic :: Internet',
          'Topic :: Utilities',
      ],
     )
