# -*- coding: utf-8 -*-
"pyloco task setup script"

if __name__ == "__main__":

    from setuptools import setup, find_packages

    __taskname__ = "shellcmd"

    setup(
        name="shellcmd",
        version="0.1.0",
        packages=find_packages(),
        package_data={},
        install_requires=["pyloco>=0.0.132"],
        entry_points = {"pyloco.task": ["{taskname} = {taskname}:entry_task".format(taskname=__taskname__)]},
    )
