import setuptools
from rvtts.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()
version = {}
with open("rvtts/version.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="rvtts",
    version=version['__version__'],
    author="Tino Khong",
    author_email="tinokhong@gmail.com",
    description="rvTTS - ResponsiveVoice TTS CLI Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tinotk/rvtts",
    packages=setuptools.find_packages(),
    keywords=['rvtts', 'responsive voice tts', 'TTS for python3' ,'text to speech for python','tts','text to speech','speech','speech synthesis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "click"
    ],
    extras_require={
        'docs': [
            'sphinx >= 1.4',
            'sphinx_rtd_theme',
            'sphinx_click']},
    entry_points={                                                              
        'console_scripts': [                                                    
            'rvtts=rvtts.rvtts:tts',                                             
        ],                                                                      
    },  
)