from setuptools import setup


setup(
    name='tisdk',
    version='0.0.2',
    description='python sdk of taiqiyun',
    long_description='pip install tisdk; tireq to_9012345678_grs 3292a4f76c0d46bf post http://taiqiyun.wowfintech.cn/grs/v1/open_match name:美团,foo:bar',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    py_modules=['ti'],
    entry_points={
        'console_scripts': ['tireq=ti:tireq'],
    },
    include_package_data=True,
)
