import setuptools,sys,os.path
try:
    from sphinx.setup_command import BuildDoc
    cmdclass = { 'doc': BuildDoc, 'cov': BuildDoc }
except ImportError:
    cmdclass = {}
from pep440nz import head_tag_description

version = head_tag_description().version()
vstring = version.str_version
rstring = version.str_release
dirty = (version.local.value is not None) and ('dirty' in version.local.value)
if dirty:
    version.local.value = list(filter(lambda x: x != 'dirty', version.local.value))
    rstring = str(version)

name = 'neze-webcli'
author='Clement Durand',
doc_opt = {
    'project': ('setup.py',name),
    'version': ('setup.py',version.str_version),
    'release': ('setup.py',version.str_release),
    'source_dir': ('setup.py','doc'),
}
cov_opt = dict(doc_opt)
cov_opt.update({
    'builder': ('setup.py','coverage'),
})

if len(sys.argv) < 2:
    if dirty:
        sys.stderr.write('Dirty tree.\n')
        sys.exit(1)
    wheel = '-'.join([name.replace('-','_'),rstring,'py3','none','any'])+'.whl'
    sdist = '-'.join([name,rstring])+'.tar.gz'
    dist = 'dist'
    print(os.path.join(dist,wheel))
    print(os.path.join(dist,sdist))
    sys.exit(0)


with open("webcli/__version__.py", "w") as vf:
    vf.write("__VERSION__='{}'\n".format(rstring))

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=rstring,
    author=author,
    author_email="durand.clement.13@gmail.com",
    description="Utility suite",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="",
    packages=setuptools.find_packages(),
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ),
    entry_points={
        'console_scripts': [
            'transmission = webcli.cli.transmission:main',
            'gitlab = webcli.cli.gitlab:main',
            'git-piptag = webcli.cli.git_piptag:main',
            'wcc = webcli.cli.wcc:main',
        ]
    },
    install_requires=['requests','PyYAML','python-dateutil','pep440nz'],
    cmdclass=cmdclass,
    command_options={
        'doc': doc_opt,
        'cov': cov_opt,
    }
)
