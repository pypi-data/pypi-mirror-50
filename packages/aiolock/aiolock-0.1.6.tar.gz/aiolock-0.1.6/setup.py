from setuptools import setup, find_packages


desc = """
do not try
"""

setup(
      name='aiolock',
      version='0.1.6',
      packages=find_packages(),
      install_requires=[
            "aioredis>=1.2.0",  # 基于这个版本写的
      ],
      description=desc,
      author='bigpangl\n\r',
      author_email='bigpangl@163.com\n\r',
      url="https://github.com/bigpangl \n\r",
      license="MIT",
)
