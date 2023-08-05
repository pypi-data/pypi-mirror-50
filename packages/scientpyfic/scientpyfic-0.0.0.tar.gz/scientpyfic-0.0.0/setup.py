from setuptools import setup
from os import path

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

setup(name='scientpyfic',
      version='0.0.0',
      description='Latest science news.',
      long_description=long_description,
      url='https://github.com/monzita/scientpyfic',
      author='Monika Ilieva',
      author_email='hidden@hidden.com',
      license='MIT',
      keywords='cli scientpyfic science python beautifulsoup',
      packages=['scientpyfic'],
      package_dir={'scientpyfic' : 'scientpyfic'},
      py_modules=['scientpyfic.commands', 'scientpyfic.commands.new'],
      install_requires = ['docopt', 'beautifulsoup4'],
      entry_points = {
        'console_scripts': [
          'scientpyfic=scientpyfic.cli:main'
        ],
      },
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Utilities'
      ],
      zip_safe=True)