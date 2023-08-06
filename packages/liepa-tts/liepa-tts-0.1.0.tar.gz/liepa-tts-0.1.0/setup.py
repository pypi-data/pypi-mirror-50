# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['liepa_tts']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0']

setup_kwargs = {
    'name': 'liepa-tts',
    'version': '0.1.0',
    'description': 'Python bindings for Lithuanian language synthesizer from LIEPA project',
    'long_description': '# [LIEPA](https://www.raštija.lt/liepa)\n\n#### Lietuvių šneka valdomos paslaugos (Lithuanian speech controlled services)\n\nThis project aims to provide high quality digital Lithuanian speech services\nfor free.\nSo far there are several services provided at various stages of completeness,\nsuch as Lithuanian speech recognizer and Lithuanian speech synthesizer.\n\nThis package wraps the latter.\n\n## Dependencies\n\nFor this package (liepa-tts) to work you need synthesizer binaries which you\'ll\nhave to compile yourself.\n\nThe original sources can be acquired [here](http://liepaatnaujinimai.rastija.lt/sintezatorius/SintezesVariklis_LIEPAprojektas.zip)\n\nTo make it easier to build binaries for platforms other than Windows you can\nacquire fixed-up sources here: [laba-diena-tts](https://github.com/OzymandiasTheGreat/laba-diena-tts)\n\nOnce you build binaries from the native-modules subtree make sure they are\navailable on LIBRARY_PATH (for building) and LD_LIBRARY_PATH (for runtime).\n\n## Installation\n\nI highly recommend [Poetry](https://poetry.eustace.io/)\n\n`poetry add liepa-tts`\n\nIf you must, use pip:\n\n`pip install liepa-tts`\n\nYou need numpy available for building C extension, so if you get errors first install that:\n\n`pip install numpy`\n\n## Usage\n\n```python\nfrom liepa_tts import liepa\n\n# All strings must be encoded with Windows Baltic encoding\nENCODING = "cp1257"\n\n# First parameter is the path to data directory\n# Second parameter is the path to voice directory\n# All paths must include trailing slash\n# Returns error code\nliepa.init("data/".encode(ENCODING), "data/Edvardas/".encode(ENCODING))\n\n# Parameters:\n# text: String that will be syntesized\n# outSize: Integer. Typically this takes ~3072 per phoneme (letter), if it\'s too small you\'ll get buffer overflow errors\n# speed: Integer. The larger the value the slower the voice will talk. Can be negative.\n# tone: Integer. The pitch. Larger values make for higher pitch. Can be negative.\n# Returns tuple (error code, ndarray). ndarray contains wav data without headers as array of integers.\ntext = "Laba diena. Kaip jums sekasi?".encode(ENCODING)\nerr, buff = liepa.synth(text, len(text) * 3072, 100, 0)\n\n# Parameters:\n# buff: The ndarray returned by liepa.synth() method\n# filename: encoded path to output file\nliepa.toWav(buff, "test.wav".encode(ENCODING))\n\n# Call this when you\'re done to free resources\nliepa.unload()\n```\n\n##### Notes:\n\nError codes produces by the synthesizer are defined in\n`include/LithUSS_Error.h` so if you need more info on\nthe error you\'re getting check that file.\n\nYou can acquire the data files along with original sources [here](http://liepaatnaujinimai.rastija.lt/sintezatorius/SintezesVariklis_LIEPAprojektas.zip)\n\nThe files that must be present in `data/` directory are:\n\n- `abb.txt`\n- `duom.txt`\n- `rules.txt`\n- `skaitm.txt`\n\nYou should extract voice directories unmodified.\n\nThe `.wav` produce by the synthesizer is completely unoptimized and contains\na lot of silence. Therefor you should further process it before usage.\n',
    'author': 'Ozymandias',
    'author_email': 'tomas.rav@gmail.com',
    'url': 'https://github.com/OzymandiasTheGreat/liepa-tts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
