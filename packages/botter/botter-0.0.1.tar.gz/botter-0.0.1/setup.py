import re

from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('src/botter/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Package version is not set")

if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:
        import subprocess
        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

readme = ''
with open('README.md') as f:
    readme = f.read()

extras_require = { }

setup \
(
    name = 'botter',
    url = 'https://gitlab.com/Hares/botter',
    version = version,
    packages =
    [
        'botter',
        'botter.api',
        'botter.api.handlers',
        'botter.util',
        'botter.discord',
    ],
    package_dir = { '': 'src' },
    license = "BSD 2-Clause License",
    description = "Python messenger bot aggregator, supporting Discord, Telegram, and potentially others",
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
    install_requires = requirements,
    extras_require = extras_require,
    python_requires = '>=3.6.0',
    classifiers =
    [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
