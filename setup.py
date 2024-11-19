from setuptools import setup, find_packages

setup(
    name="clip",
    version="1.0.0",
    author="Teemu Tallskog",
    description="A tool to split videos between two timestamps.",
    packages=find_packages(),
    py_modules=["clip"],
    install_requires=[
        "moviepy>=1.0.3"
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "clip=clip.clip:main",
        ]
    },
)