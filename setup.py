from setuptools import setup

setup(name='gt',
      version='0.0.1',
      description='Google Translate library and clients',
      author='shdown',
      author_email='shdownnine@gmail.com',
      url='https://github.com/shdown/gt',
      license='LGPLv3',
      packages=['gt', 'gt_clients'],
      extras_require={
          'gt_notify': ['notify2'],
          'gt_notify_see_also': ['gi'],
      },
      entry_points={
          'console_scripts': ['gt = gt_clients.gt_console:main',
                              'gt_notify = gt_clients.gt_notify:main',
                             ],
      },
      scripts=['gt_play'],
     )
