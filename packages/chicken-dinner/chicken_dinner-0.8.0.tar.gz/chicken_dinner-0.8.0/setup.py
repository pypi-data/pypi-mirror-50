# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chicken_dinner',
 'chicken_dinner.assets',
 'chicken_dinner.models',
 'chicken_dinner.models.match',
 'chicken_dinner.models.telemetry',
 'chicken_dinner.pubgapi',
 'chicken_dinner.visual']

package_data = \
{'': ['*'],
 'chicken_dinner.assets': ['maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Baltic_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/Desert_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/DihorOtok_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Erangel_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Range_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png',
                           'maps/Savage_Main_Low_Res.png']}

install_requires = \
['requests>=2.22,<3.0']

extras_require = \
{'visual': ['matplotlib>=3.1,<4.0', 'pillow>=6.1,<7.0']}

setup_kwargs = {
    'name': 'chicken-dinner',
    'version': '0.8.0',
    'description': 'PUBG JSON API Wrapper and Game Telemetry Visualizer',
    'long_description': 'Chicken Dinner\n==============\n\n|rtd| |pypi| |pyversions|\n\n.. |rtd| image:: https://img.shields.io/readthedocs/chicken-dinner.svg\n    :target: http://chicken-dinner.readthedocs.io/en/latest/\n\n.. |pypi| image:: https://img.shields.io/pypi/v/chicken-dinner.svg\n    :target: https://pypi.python.org/pypi/chicken-dinner\n\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/chicken-dinner.svg\n    :target: https://pypi.python.org/pypi/chicken-dinner\n\nPython PUBG JSON API Wrapper and (optional) playback visualizer.\n\nSamples\n-------\n\n* `Erangel - squads <http://chicken-dinner.readthedocs.io/en/latest/sample_erangel.html>`_\n* `Miramar - solos <http://chicken-dinner.readthedocs.io/en/latest/sample_miramar.html>`_\n* `Sanhok - duos <http://chicken-dinner.readthedocs.io/en/latest/sample_sanhok.html>`_\n* `Vikendi - duos <http://chicken-dinner.readthedocs.io/en/latest/sample_vikendi.html>`_\n\nInstallation\n------------\n\nTo install chicken-dinner, use pip. This will install the core dependencies\n(``requests`` library) which provide functionality to the API wrapper classes.\n\n.. code-block:: bash\n\n    pip install chicken-dinner\n\nTo use the playback visualizations you will need to install the library with\nextra dependencies for plotting (``matplotlib`` and ``pillow``).\nFor this you can also use pip:\n\n.. code-block:: bash\n\n    pip install chicken-dinner[visual]\n\nTo generate the animations you will also need ``ffmpeg`` installed on your\nmachine. On Max OSX you can install ``ffmpeg`` using brew.\n\n.. code-block:: bash\n\n    brew install ffmpeg\n\nYou can install ffmpeg on other systems from `here <https://www.ffmpeg.org/download.html>`_.\n\nUsage\n-----\n\nWorking with the low-level API class.\n\n.. code-block:: python\n\n    from chicken_dinner.pubgapi import PUBGCore\n\n    api_key = "your_api_key"\n    pubgcore = PUBGCore(api_key, "pc-na")\n    shroud = pubgcore.players("player_names", "shroud")\n    print(shroud)\n\n    # {\'data\': [{\'type\': \'player\', \'id\': \'account.d50f...\n\nWorking with the high-level API class.\n\n.. code-block:: python\n\n    from chicken_dinner.pubgapi import PUBG\n\n    api_key = "your_api_key"\n    pubg = PUBG(api_key, "pc-na")\n    shroud = pubg.players_from_names("shroud")[0]\n    shroud_season = shroud.get_current_season()\n    squad_fpp_stats = shroud_season.game_mode_stats("squad", "fpp")\n    print(squad_fpp_stats)\n\n    # {\'assists\': 136, \'boosts\': 313, \'dbnos\': 550, \'daily_kills\':...\n\nVisualizing telemetry data\n\n.. code-block:: python\n\n    from chicken_dinner.pubgapi import PUBG\n\n    api_key = "your_api_key"\n    pubg = PUBG(api_key, "pc-na")\n    shroud = pubg.players_from_names("shroud")[0]\n    recent_match_id = shroud.match_ids[0]\n    recent_match = pubg.match(recent_match_id)\n    recent_match_telemetry = recent_match.get_telemetry()\n    recent_match_telemetry.playback_animation("recent_match.html")\n\nRecommended playback settings:\n\n.. code-block:: python\n\n    telemetry.playback_animation(\n        "match.html",\n        zoom=True,\n        labels=True,\n        label_players=[],\n        highlight_winner=True,\n        label_highlights=True,\n        size=6,\n        end_frames=60,\n        use_hi_res=False,\n        color_teams=True,\n        interpolate=True,\n        damage=True,\n        interval=2,\n        fps=30,\n    )\n\nSee the `documentation <http://chicken-dinner.readthedocs.io>`_ for more\ndetails.\n',
    'author': 'Christopher Flynn',
    'author_email': 'crf204@gmail.com',
    'url': 'https://github.com/crflynn/chicken-dinner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
