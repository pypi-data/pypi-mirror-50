from __future__ import absolute_import

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


setup(name='datadog_metrics',
      description='A tool for generating code from templates',
      version='0.0.0',
      python_requires='>=2.7.12',
      packages=['datadog_metrics'],
      entry_points={
          'console_scripts': [
              'datadog_metrics = datadog_metrics.main:main'
          ],
      },
      include_package_data=True,
      install_requires=[
          'datadog',
          'peloconfig',
          'splunk-http-logger'
      ],
      setup_requires=["pytest-runner"],
      tests_require=[
          "pytest >= 4.6.3"
      ]
      )

