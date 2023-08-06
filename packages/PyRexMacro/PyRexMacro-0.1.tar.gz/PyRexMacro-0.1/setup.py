from setuptools import setup
 
setup(
  name='PyRexMacro',             # This is the name of your PyPI-package.
  py_modules=['pyrex'],
  version='0.1',            # Update the version number for new releases
  description = "Text Macro Preprocessor, especially good for javascript, etc.",
  author = "Steve Beisner",
  author_email = "beisner@alum.mit.edu",
  url = "https://github.com/stevebeisner/PyRex",
  keywords = ["templates", "python server pages"],
  classifiers = [
      "Programming Language :: Python :: 3 :: Only",
      "Development Status :: 3 - Alpha",
      "Environment :: Console",
      "Environment :: Other Environment",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Topic :: Text Processing"
      ],
    long_description = """\
PyRex Macro Preprocessor
------------------------
 Especially useful for javascript, where one doesn't want to change the line
 numbers of input lines:  lines in the output will be at the same line # position
 as they were in the original input file!
"""
)