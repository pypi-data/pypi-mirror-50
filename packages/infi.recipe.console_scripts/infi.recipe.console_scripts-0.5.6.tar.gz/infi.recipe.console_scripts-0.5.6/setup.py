
SETUP_INFO = dict(
    name = 'infi.recipe.console_scripts',
    version = '0.5.6',
    author = 'Arnon Yaari',
    author_email = 'arnony@infinidat.com',

    url = 'https://github.com/Infinidat/infi.recipe.console_scripts',
    license = 'BSD',
    description = """buildout recipe for generating better console and gui script for entry points""",
    long_description = """buildout recipe for generating better console and gui script for entry points""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'setuptools>=32.0',
'zc.buildout'
],
    namespace_packages = ['infi', 'infi.recipe'],

    package_dir = {'': 'src'},
    package_data = {'': [
'embed-gui-x64.exe',
'embed-gui-x86.exe',
'embed-x64.exe',
'embed-x86.exe',
'embed3-gui-x64.exe',
'embed3-gui-x86.exe',
'embed3-x64.exe',
'embed3-x86.exe',
'Microsoft.VC90.CRT.manifest-x64',
'Microsoft.VC90.CRT.manifest-x86',
'msvcm90.dll-x64',
'msvcm90.dll-x86',
'msvcp90.dll-x64',
'msvcp90.dll-x86',
'msvcr90.dll-x64',
'msvcr90.dll-x86'
]},
    include_package_data = True,
    zip_safe = False,

    entry_points = {
        'console_scripts': ['console-script-test = infi.recipe.console_scripts:nothing', 'replace_gui_script = infi.recipe.console_scripts.windows:replace_gui_script', 'replace_console_script = infi.recipe.console_scripts.windows:replace_console_script'],
        'gui_scripts': ['gui-script-test = infi.recipe.console_scripts:nothing'],
        'zc.buildout': ['default = infi.recipe.console_scripts:Scripts',
                        'script = infi.recipe.console_scripts:Scripts',
                        'scripts = infi.recipe.console_scripts:Scripts',
                        'gui_script = infi.recipe.console_scripts:GuiScripts',
                        'gui_scripts = infi.recipe.console_scripts:GuiScripts',]
        }
    )

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

