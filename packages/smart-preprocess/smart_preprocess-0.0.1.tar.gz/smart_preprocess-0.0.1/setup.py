from setuptools import setup, find_packages
from os import listdir
from os.path import isfile, join
ttps = [f for f in listdir('smart_preprocess/help') if isfile(join('smart_preprocess/help', f))]
ttps = [''.join(('smart_preprocess/',f)) for f in ttps]
dm = [f for f in listdir('smart_preprocess/dmreader') if isfile(join('smart_preprocess/dmreader', f))]
dm = [''.join(('smart_preprocess/',f)) for f in dm]
print(ttps)
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="smart_preprocess",
    version="0.0.1",
    author="Joshua Stuckner",
    author_email="stuckner@vt.edu",
    description="A package for denoising TEM video data.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JStuckner/smart_preprocess/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['tkinter',
                      'numpy',
                      'matplotlib',
                      'h5py',
                      'scipy',
                      'scikit-image',
                      'pil'],
    package_data={'help': ttps,
                  'dmreader': dm,},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
