from setuptools import setup, find_packages

setup(
    name='audio-cutter',
    version='0.1',
    packages=find_packages(),
    install_requires=["pydub", "pytest",
                      "git+https://github.com/ytdl-org/youtube-dl.git"],
)
