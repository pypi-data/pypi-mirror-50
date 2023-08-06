try:
    from setuptools import setup
except ImportError:
    # Fallback to standard library distutils.
    from distutils.core import setup

setup(
    name='git-phoenix',
    version='1.0.0-beta37',
    description='phoenix',
    long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
    author='victoraugustofd',
    author_email='victoraugustofd@gmail.com',
    license='MIT',
	packages=['git_phoenix'],
    url='https://github.com/victoraugustofd/git-phoenix',
    scripts = [
        'bin/git-phoenix'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
)
