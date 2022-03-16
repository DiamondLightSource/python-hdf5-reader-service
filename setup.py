# type: ignore
import glob
import importlib.util

from setuptools import setup

# Import <package>._version_git.py without importing <package>
path = glob.glob(__file__.replace("setup.py", "src/*/_version_git.py"))[0]
spec = importlib.util.spec_from_file_location("_version_git", path)
vg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vg)

setup(cmdclass=vg.get_cmdclass(), version=vg.__version__)

setup(
    name="example",
    version="0.1.0",
    install_requires=[
        "anyio==3.5.0",
        "asgiref==3.4.1",
        "attrs==21.4.0",
        "cached-property==1.5.2",
        "certifi==2021.10.8",
        "charset-normalizer==2.0.12",
        "click==8.0.3",
        "contextlib2==21.6.0",
        "contextvars==2.4",
        "defusedxml==0.7.1",
        "fastapi==0.74.1",
        "h11==0.13.0",
        "h5py==3.1.0",
        "httpie==2.6.0",
        "idna==3.3",
        "immutables==0.16",
        "importlib-metadata==4.2.0",
        "iniconfig==1.1.1",
        "itsdangerous==2.0.1",
        "MarkupSafe==2.0.1",
        "mccabe==0.6.1",
        "numpy==1.19.5",
        "orjson==3.6.1",
        "packaging==21.3",
        "pathspec==0.9.0",
        "platformdirs==2.4.0",
        "pluggy==1.0.0",
        "py==1.11.0",
        "pydantic==1.9.0",
        "pyflakes==2.4.0",
        "Pygments==2.11.2",
        "pyparsing==3.0.7",
        "PySocks==1.7.1",
        "pytest==7.0.1",
        "requests==2.27.1",
        "requests-toolbelt==0.9.1",
        "sniffio==1.2.0",
        "starlette==0.17.1",
        "tomli==1.2.3",
        "typing_extensions==4.1.1",
        "urllib3==1.26.8",
        "uvicorn==0.16.0",
        "Werkzeug==2.0.3",
<<<<<<< HEAD
        "zipp==3.6.0",
    ],
=======
        "zipp==3.6.0"
    ]
>>>>>>> 4a3821a14ff3f44e8de43bf3786bd8d67c086e7e
)
