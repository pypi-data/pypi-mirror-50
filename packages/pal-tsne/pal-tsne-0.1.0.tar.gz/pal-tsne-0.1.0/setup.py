import os
from setuptools import setup, find_packages


path = os.path.abspath(os.path.dirname(__file__))

try:
  with open(os.path.join(path, 'README.md')) as f:
    long_description = f.read()
except Exception as e:
  long_description = "customize okta cli"

setup(
    name = "pal-tsne",
    version = "0.1.0",
    keywords = ("pip", "tsne", "parallel", "xenos"),
    description = "parallel tsne",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6.0",
    license = "MIT Licence",

    url = "https://github.com/MingChaoXu/paralell-tsne",
    author = "xenos",
    author_email = "mingchao.xu.casia@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    install_requires = ["requests", "click"],
    platforms = "any",

    scripts = [],
    entry_points = {
        'console_scripts': [
            'pal-tsne=tsne.cli:main_cli'
        ]
    }
)