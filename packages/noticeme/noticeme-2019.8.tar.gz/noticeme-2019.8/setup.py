from setuptools import setup, find_packages

from os import path
cwd = path.abspath(path.dirname(__file__))
with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='noticeme',
      description=("Provides a framework for building file watchers."
                   " Includes a file watcher utility program"
                   " that allows you to create file watchers declaratively."),
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/bobbytrapz/noticeme',
      author='Bobby',
      author_email='bobbytrapz@protonmail.com',
      license='MIT',
      version='2019.8',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'noticeme = noticeme.__main__:main',
          ]
      },
      python_requires='>=3.5',
      setup_requires=["cffi>=1.0.0"],
      install_requires=["cffi>=1.0.0"],
      cffi_modules=["noticeme/inotify_build.py:ffibuilder"],
      keywords='inotify watch development',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Build Tools',
          'Topic :: System :: Filesystems',
      ])
