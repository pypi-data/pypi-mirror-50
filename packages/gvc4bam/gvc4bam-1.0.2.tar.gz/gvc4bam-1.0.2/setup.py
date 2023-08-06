# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
import os
# or
# from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README')) as f:
    README = f.read()

setup(
    name='gvc4bam',     # 包名字
    version='1.0.2',   # 包版本
    description='This is a tools of writing vcf',   # 简单描述
    author='LongHui.Yin',  # 作者
    author_email='dragonfly.yin@genowis.com',  # 作者邮箱
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),                 # 包
    install_requires=['docker==2.5.1', 'pysam', 'toil', 'toil-runner'],
    scripts=['tools/bam_vcf.py','gvc4bam/gvc_vcf_pipeline.py','tools/check_runtime.py']
)
