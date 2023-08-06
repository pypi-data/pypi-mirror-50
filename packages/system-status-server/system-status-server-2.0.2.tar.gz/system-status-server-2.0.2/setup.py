from setuptools import setup, find_packages

setup(
    name = "system-status-server",
    version = '2.0.2',
    description = "This is a very lightweight stuff to get some system status info in JSON.",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/system-status-server',
    license = 'MIT',
    install_requires = [
        "psutil~=5.6",
        "Flask~=1.0",
        "prettytable~=0.7",
    ],
    packages = find_packages(),
    scripts = [
        "bin/hdd-stat",
    ],
)
