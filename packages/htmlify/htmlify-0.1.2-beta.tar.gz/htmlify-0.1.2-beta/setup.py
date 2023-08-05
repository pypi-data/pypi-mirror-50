from distutils.core import setup

long_description = """# htmlify
An ultra-basic, human-friendly templating system for doing CGI with Python for less 😕 and more 🎉

htmlify is powerful enough to drive small web projects, while lightweight enough that you don't feel like you're learning a whole new language. See the [GitHub page](https://github.com/iDoObject/htmlify) for more info and an installation/usage guide."""

setup(
  name = 'htmlify',
  packages = ['htmlify'],
  version = '0.1.2-beta',
  license='MIT',
  description = 'An ultra-basic, human-friendly templating system for doing CGI with Python for less 😕 and more 🎉',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Theo Court',
  author_email = 'theo.court@pm.me',
  url = 'https://github.com/iDoObject/htmlify',
  download_url = 'https://github.com/iDoObject/htmlify/archive/v0.1.2-beta.tar.gz',
  keywords = ['CGI', 'python3', 'HTML', 'templates', 'templating'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)