import setuptools
import os

with open(os.path.join('cudam', "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cudam",
    version="0.0.1",
    author="Bin Wang",
    author_email="wwwbbb8510@gmail.com",
    description="Cuda Mangement - multi-process, scheduled jobs, distributed processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wwwbbb8510/cudam.git",
    packages=setuptools.find_packages(),
    scripts=[
        'cudam/bin/cudam_snap_gpu.py',
        'cudam/bin/cudam_task_manager.py'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)