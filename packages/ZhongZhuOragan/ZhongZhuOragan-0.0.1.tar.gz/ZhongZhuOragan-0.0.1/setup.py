# # 引入构建包信息的模块
# from distutils.core import setup
# from setuptools import setup

# # 定义发布的包文件的信息
# setup(
#     name="OrganSDK",  # 发布的包的名称
#     version="1.00.003",  # 发布包的版本序号
#     description="机构上报",  # 发布包的描述信息
#     author="zhm",  # 发布包的作者信息
#     # author_email="1847562860@qq.com",  # 作者的联系邮箱
#     py_modules=['OrganClient', 'PageQuery', 'HttpClientHelper']  # 发布包中的模块文件列表
# )
from setuptools import setup, find_packages

# setup(
#     name='GFICLEE',
#     version="1.00.003",
#     packages=find_packages(),
#     # entry_points={
#     #     "console_scripts": ['GFICLEE = predict.main:main']
#     # },
#     # install_requires=[
#     #     "numpy==1.14.3",
#     #     "pandas==0.22.0",
#     # ],
#      url='https://github.com/yangfangs/GFICLEE',
#     # license='GNU General Public License v3.0',
#     author='Yang　Fang',
#     author_email='yangfangscu@gmail.com',
#     description='Gene function inferred by common loss evolution events'
# )
setup(
    name='ZhongZhuOragan',  # 包名
    python_requires='>=3.4.0',  # python环境
    version='0.0.1',  # 包的版本
    description="ZhongZhuOragan",
    # long_description=read_file('README.md'),  # 读取的Readme文档内容
    # long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="tianlianpei",  # 作者相关信息
    author_email='tianlianpei@zhongzhudata.com',
    url='https://developer.zhujianyun.com',
    # 指定包信息，还可以用find_packages()函数
    packages=find_packages(),
    # packages=[
    #     'Organ',
    #     'Organ.organClient.py'
    # ],
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    include_package_data=True,
    # license="MIT",
    keywords=['organclient'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
