from setuptools import setup, find_packages


with open("README.md","r") as f:
      description = f.read()
      setup(
            name='aiolock',
            version='0.1.1',
            packages=find_packages(),
            install_requires=[
                  "aioredis>=1.2.0",  # 基于这个版本写的
            ],

            description=description,
            author='bigpangl',
            author_email='bigpangl@163.com',
            url="https://github.com/bigpangl",
            license="MIT",
      )
