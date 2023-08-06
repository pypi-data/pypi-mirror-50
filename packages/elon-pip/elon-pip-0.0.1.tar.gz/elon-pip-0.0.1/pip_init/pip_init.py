# -*- coding: utf-8 -*-


import os

code = '''
# -*- coding: utf-8 -*-

def exe():
    pass

'''

gitignore_content = '''
**/dist
**/*.egg-info
**/__pycache__
**/.idea
'''




def gen_setup_content():
    setup_content = '''
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(
    name='xxx',
    version="0.0.1",
    keywords=("elon"),
    description="xxx",
    long_description="xxx",
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
    install_requires=['twine'],

    entry_points={
        'console_scripts': [
            'cmd_xxx = xxx.main:exe',
        ]
    },
)
    
    '''
    return setup_content


def exe():
    name = input('名称:')
    setup_path = os.path.join(name, 'setup.py')
    gitignore_path = os.path.join(name, '.gitignore')

    code_dir_path = os.path.join(name, name)
    init_path = os.path.join(code_dir_path, '__init__.py')
    main_path = os.path.join(code_dir_path, 'main.py')

    if not os.path.exists(code_dir_path):
        os.makedirs(code_dir_path)

    with open(setup_path, 'w') as f:
        f.writelines([gen_setup_content(), ])

    with open(init_path, 'w') as f:
        f.writelines(['# -*- coding: utf-8 -*-', ])

    with open(main_path, 'w') as f:
        f.writelines([code, ])

    with open(gitignore_path, 'w') as f:
        f.writelines([gitignore_content, ])


