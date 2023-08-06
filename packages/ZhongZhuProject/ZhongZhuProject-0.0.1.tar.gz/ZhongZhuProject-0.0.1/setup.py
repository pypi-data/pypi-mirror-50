
from setuptools import setup, find_packages

setup(
    name='ZhongZhuProject',  # 包名
    python_requires='>=3.4.0',  # python环境
    version='0.0.1',  # 包的版本
    description="ZhongZhuProject",
    author="tianlianpei",  # 作者相关信息
    author_email='tianlianpei@zhongzhudata.com',
    url='https://developer.zhujianyun.com',
    # 指定包信息，还可以用find_packages()函数
    packages=find_packages(),
    include_package_data=True,
    keywords=['projectclient'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
