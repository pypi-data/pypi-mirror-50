from setuptools import setup, find_packages


with open("README.md","r") as f:
      description = f.read()
      setup(
            name='aiolock',
            version='0.1.2',
            packages=find_packages(),
            install_requires=[
                  "aioredis>=1.2.0",  # 基于这个版本写的
            ],

            description=description,
            author='\n\rbigpangl',
            author_email='\n\rbigpangl@163.com',
            url="\r\nhttps://github.com/bigpangl",
            license="MIT",
      )
