import os.path
import setuptools


if __name__ == "__main__":
    dir_path = os.path.dirname(__file__)
    readme_path = os.path.abspath(os.path.join(dir_path, "README.rst"))
    with open(readme_path) as readme_file:
        long_description = readme_file.read()

    setuptools.setup(
        name="lila",
        version="0.0.1",
        author="KillAChicken",
        author_email="KillAChicken@yandex.ru",
        description="Library to work with Siren protocol",
        long_description=long_description,
        url="https://github.com/KillAChicken/lila",
        packages=setuptools.find_packages(include=("lila*", )),
        install_requires=[
            ],
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            ],
        )
