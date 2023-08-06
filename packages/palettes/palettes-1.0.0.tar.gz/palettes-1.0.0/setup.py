from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='palettes',
      version='1.0.0',
      description='Random Hex Color Codes',
      url='https://github.com/SafyreLyons/palettes',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Safyre Lyons',
      author_email='lyons.safyre@gmail.com',
      license='The Unlicence',
      py_modules=['app'],
      package_dir={'': 'src'},
      zip_safe=False)