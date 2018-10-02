import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="djangosmartshare",
    version="0.8.7",
    author="Abolfazl Amiri",
    author_email="aa.smpro@gmail.com",
    description="simple django app for sharing files over http / https.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aasmpro/djangosmartshare",
    packages=setuptools.find_packages(exclude=['smartshareserver']),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
