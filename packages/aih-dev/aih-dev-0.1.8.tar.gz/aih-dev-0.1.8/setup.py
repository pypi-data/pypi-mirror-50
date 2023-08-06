from setuptools import setup

setup(name='aih-dev',
      version='0.1.8',
      description='',
      author='dien.duong',
      author_email='duongngocdien@gmail.com',
      license='MIT',
      packages=['aih', 'utils'],
      install_requires=[
            'PyJWT',
            'requests',
            'opencv-python',
            'opencv-contrib-python',
            'Pillow'
      ],
      zip_safe=False)
