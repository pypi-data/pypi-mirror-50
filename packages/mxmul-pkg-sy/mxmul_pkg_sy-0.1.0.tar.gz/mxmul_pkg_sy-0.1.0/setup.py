#格式化程序
import setuptools
'''打开文本文件作为一个长描述的引用
路径无需打全，命令行中①d:②chdir 目录路径D:\PYECourse\mxmul_st
, encoding='UTF-8',避免报错UnicodeDecodeError: 'gbk' codec can't decode byte 0xa8 in position 53: illegal multibyte sequence'''
with open('README.md','r',encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(  #各部分尽量填写，空着也行
    name = 'mxmul_pkg_sy',
    version = '0.1.0',
    author = 'sy',
    author_email = 'phy1818@126.com',
    description = 'An example for testing how to publish a Python package',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/pypa/sampleproject',
    package = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)