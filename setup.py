from pathlib import Path

import setuptools

HERE = Path(__file__).parent

def get_content(path: str) -> str:
    with open(HERE / path, encoding="utf8") as file:
        return file.read()

REQUIRES = get_content("requirements.txt")
DEV_REQUIRES = get_content("requirements_dev.txt") + REQUIRES
setuptools.setup(
    install_requires=REQUIRES,
    tests_require=DEV_REQUIRES,
    extras_require={"dev": DEV_REQUIRES},
    package_data={"": ["requirements.txt", "requirements_dev.txt"]},
    version="0.1.0",
)
