@echo off


:start
cls

set python_ver=36

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install aiofiles
pip install beautifulsoup4
pip install discord.py
pip install Pillow
pip install requests
pip install selenium
pip install webdriver-manager

pause
exit