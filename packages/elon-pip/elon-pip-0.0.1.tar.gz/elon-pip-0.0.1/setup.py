from setuptools import setup, find_packages

setup(
    # pip install nnn
    name="elon-pip",
    version="0.0.1",
    keywords=("elon"),
    description="pip init template, commmand: pipinit",
    long_description="pip init template commmand: pipinit",
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
            'pipinit = pip_init.pip_init:exe',
        ]
    },

)
