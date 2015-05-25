from distutils.core import setup

setup(name='gt',
      version='0.0.1',
      description='Google Translate library and clients',
      author='shdown',
      author_email='shdownnine@gmail.com',
      url='https://github.com/shdown/gt',
      license='LGPLv3',
      packages=['gt'],
      scripts=['gt_console', 'gt_notify', 'gt_dump_json', 'gt_play',
               'gt_shell'],
     )
