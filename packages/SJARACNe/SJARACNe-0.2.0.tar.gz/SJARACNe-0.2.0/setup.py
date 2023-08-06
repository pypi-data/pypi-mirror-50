import sys
from setuptools import setup, find_packages
from distutils.command.install import install
from distutils.command.build import build
from subprocess import call

class Build(build):
    def run(self):
        cmd = ["make", "-C", "./SJARACNe"]
        if call(cmd) != 0:
            sys.exit(-1)
        build.run(self)

version = {}
with open("./version.py") as fp:
    exec(fp.read(), version)

setup(
    name="SJARACNe",
    version=version["__version__"],
    description="Gene network reverse engineering from big data",
    url="https://github.com/jyyulab/SJARACNe",
    author="Liang Ding, Chenxi Qian, Jiyang Yu",
    author_email="liang.ding@stjude.org, chenxi.qian@stjude.org, jiyang.yu@stjude.org",
    license="See LICENSE.md",
    install_requires=[
        "pandas >= 0.22.0",
        "numpy >= 1.14.2",
        "scipy == 1.0.1",
        "cwltool == 1.0.20190618201008",
    ],
    python_requires="==3.6.1",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    include_package_data=True,
    # test_suite="tests",
    entry_points={"console_scripts": ["sjaracne=SJARACNe.sjaracne:main"]},
    cmdclass={
        'build': Build,
    }
)
