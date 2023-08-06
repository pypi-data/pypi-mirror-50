from setuptools import setup, find_packages

setup(
    # pip install nnn
    name="elon-kindle",
    version="0.0.10",
    keywords=("elon"),
    description="send to kindle",
    long_description="send to kindle",
    # 协议
    license="GPL Licence",

    url="https://github.com/elon",
    author="elon",
    author_email="elon@126.com",

    # 自动查询所有"__init__.py"
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    # 提示前置包
    # install_requires=['pandas', 'numpy', 'sqlalchemy'],

    entry_points={
        'console_scripts': [
            'kindle = kindle.kindle:send',
        ]
    },

)
