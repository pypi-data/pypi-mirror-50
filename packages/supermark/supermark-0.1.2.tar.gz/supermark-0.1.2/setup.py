from distutils.core import setup
setup(
  name='supermark',
  packages=['supermark'],
  version='0.1.2',
  description='Pandoc-based transformation tool for documents containing different markup languages.',
  install_requires=['pypandoc', 'pyyaml', 'colorama', 'click', 'openpyxl', 'progressbar2'],
  package_data={
        '': ['*.tex', '*.pdf'],
    },
  include_package_data=True,
  author='Frank Alexander Kraemer',
  author_email='kraemer.frank@gmail.com',
  license='GPLv3',
  url='https://github.com/falkr/supermark',
  download_url='https://github.com/falkr/supermark/archive/0.2.tar.gz',
  keywords=['education'],
  classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'],
  entry_points = {'console_scripts': ['supermark=supermark.command:run']}
)
