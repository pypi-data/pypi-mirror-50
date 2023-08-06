# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name='createdate',
    version='1.0.0',
    description='it is for person',
    long_description='use for person',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    install_requires=[],    # install_requires字段可以列出依赖的包信息，用户使用pip或easy_install安装时会自动下载依赖的包
    author='jianzhong.zhou',
    url='https://github.com',
    author_email='1329870572@qq.com',
    license='MIT',
    packages=['createdate'],   # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    zip_safe=True,
    package_data={
        'createdate': ['config.ini', 'test.xlsx',]
    },
    #data_files=[('createdate', ['createdate/config.ini', 'createdate/test.xlsx'])],
    # py_modules=['test_package'],
    package_dir={'createdate': 'createdate'},
)