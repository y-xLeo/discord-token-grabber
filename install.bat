@echo off


:start
cls
title Installing Discord QR Dependencies
cls
color 9
echo Installing Discord QR dependencies..
echo ----------------------------------------------------------------
echo Dont forget to set your token in the main.py file
echo Dont forget to set your webhook in Cogs  Verify.py
echo Make sure your Bot has all intens enabled.
echo For Support add me on discord...
timeout /t 10
cd \
cd \python%python_ver%\Scripts\
pip install aiofiles
pip install beautifulsoup4
pip install discord.py
pip install Pillow
pip install requests
pip install selenium
pip install webdriver-manager
pip install pipwin
pipwin install cairocffi
pip install lxml
pip install cairosvg
pause
exit