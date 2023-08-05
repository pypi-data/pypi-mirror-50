import runpy
from setuptools import setup, find_packages

PACKAGE_NAME = "avstudio"
VERSION = "2.0"

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = []
    for r in f.readlines():
        r = r.strip()
        if len(r) > 0 and r[0] != '#':
            requirements.append(r)

if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        packages=find_packages(),
        install_requires=requirements,
        python_requires=">=2.7",
        description="Python wrappers for AV Studio public API",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/epiphan-video/avstudio_api",
        author="Vadim Kalinskiy",
        author_email="vkalinsky@epiphan.com",
        keywords="avstudio",
        project_urls={
            "Documentation": "https://epiphan-video.github.io/avstudio_api"
        },
        license="MIT"
    )
