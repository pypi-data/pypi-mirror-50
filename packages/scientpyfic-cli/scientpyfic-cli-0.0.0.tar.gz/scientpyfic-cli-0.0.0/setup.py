from setuptools import setup
from os import path

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

setup(name='scientpyfic-cli',
      version='0.0.0',
      description='Latest science news on your prompt/shell.',
      long_description=long_description,
      url='https://github.com/monzita/scientpyfic-cli',
      author='Monika Ilieva',
      author_email='hidden@hidden.com',
      license='MIT',
      keywords='cli scientpyfic science daily python beautifulsoup',
      packages=['scientpyfic_cli'],
      package_dir={'scientpyfic_cli' : 'scientpyfic_cli'},
      py_modules=[],
      install_requires = ['docopt', 'beautifulsoup4', 'requests', 'lxml'],
      entry_points = {
        'console_scripts': [
          'scientpyfic_cli=scientpyfic_cli.cli:main'
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