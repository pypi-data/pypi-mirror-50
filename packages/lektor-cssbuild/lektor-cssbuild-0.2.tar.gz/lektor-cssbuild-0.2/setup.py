from setuptools import setup, find_packages


with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.txt") as changelog_file:
    changelog = changelog_file.read()

setup(
    name="lektor-cssbuild",
    version="0.2",
    description="A Lektor plugin for building CSS files",
    long_description=readme + "\n\n" + changelog,
    url="https://github.com/uyar/lektor-cssbuild",
    author="H. Turgut Uyar",
    author_email="uyar@tekir.org",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Lektor",
        "License :: OSI Approved :: BSD License",
    ],
    keywords="lektor plugin static-site CMS sass uncss cssmin",
    py_modules=["lektor_cssbuild"],
    entry_points={
        "lektor.plugins": ["cssbuild = lektor_cssbuild:CSSBuildPlugin"]
    },
)
