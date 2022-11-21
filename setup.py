# coding: utf-8

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme_content = open(os.path.join(here, "README.md")).read()

_pkg_name = "hanabi"
_description = "A reinforcement learning agent that plays hanabi"

if __name__ == "__main__":
    setup(
        name="hanabi",
        version="0.0.1",
        description=_description,
        long_description=readme_content,
        author="MadaraUchiha",
        author_email="@",
        url="https://github.com/MadaraUchiha-314/hanabi-bot",
        license="MIT",
        install_requires=["tabulate"],
        packages=["hanabi"],
        entry_points={
            "console_scripts": [
                "hanabi = hanabi.run:run_game"
            ]
        },
        include_package_data=True,
        zip_safe=False,
        test_suite="",
        classifiers=[
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: Implementation :: PyPy",
        ],
    )
