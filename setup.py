from setuptools import setup, find_packages

setup(
    name="clip",
    version="1.0.0",
    author="Teemu Tallskog",
    description="A tool to split videos between two timestamps.",
    packages=find_packages(),
    py_modules=["clip"],
    install_requires=[
        "moviepy>=1.0.3",
        "opencv-python>=4.10.0.0",
        "pillow>=11.0.0"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "clip=clip.clip:main",
        ]
    },
)