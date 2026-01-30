from setuptools import setup, find_packages

setup(
    name="wlfwifi",
    version="1.0.0",
    description="Modern, modular, and automated wireless network auditor (WEP/WPA/WPS)",
    author="Mike, derv82, ballastsec, contributors",
    author_email="",
    url="https://github.com/yourusername/wlfwifi",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "wlfwifi = wlfwifi.core:main"
        ]
    },
    include_package_data=True,
    license="GPLv2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
    ],
)