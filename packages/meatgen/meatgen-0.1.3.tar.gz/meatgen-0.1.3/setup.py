import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='meatgen',
      version='0.1.3',
      description="Generate passwords via real world phenomena",
      long_description_content_type="text/markdown",
      long_description=long_description,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
      url='http://github.com/buckley-w-david/Meatspace-password-generator',
      author='David Buckley',
      author_email='buckley.w.david@gmail.com',
      license='UNLICENSE',
      packages=['meatgen'],
      install_requires=[],
      entry_points={
          'console_scripts': ['meatgen=meatgen.cli:main'],
      },
      include_package_data=True,
      zip_safe=False
)
