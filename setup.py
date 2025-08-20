from setuptools import setup, find_packages

setup(
    name="group-files-archiver",
    version="0.1.0",
    description="Tool to archive files of user group members",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=["tqdm>=4.67.1"],
    entry_points={
        "console_scripts": [
            "group-files-archiver=group_files_archiver.main:main"
        ]
    },
)
