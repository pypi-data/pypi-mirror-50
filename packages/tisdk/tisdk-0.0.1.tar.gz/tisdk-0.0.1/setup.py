from setuptools import setup


setup(
    name='tisdk',
    version='0.0.1',
    description='tisdk',
    long_description='pip install tisdk; ti to_9012345678_grs 3292a4f76c0d46bf post http://taiqiyun.wowfintech.cn/grs/v1/open_match name:美团,foo:bar',
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='ti',
    author='tao.py',
    author_email='taojy123@163.com',
    license='MIT',
    py_modules=['ti'],
    entry_points={
        'console_scripts': ['tireq=ti:ti_request'],
    },
    include_package_data=True,
    zip_safe=False,
)
