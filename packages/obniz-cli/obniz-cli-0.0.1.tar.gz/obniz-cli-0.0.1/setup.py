from setuptools import setup

setup(
    name='obniz-cli',
    version='0.0.1',
    description='cli tool for obnizOS setup',
    # url='',
    install_requires=["esptool"],
    entry_points={
        "console_scripts": [
            "obniz_cli=obniz_cli:main"
        ]
    }
)