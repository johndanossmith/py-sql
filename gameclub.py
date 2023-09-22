from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import soundfile
import speech_recognition as sr
import os
import random
import urllib
import pandas as pd
import certifi
import math
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master
        self.pack(fill=BOTH, expand=1)

        self.var = IntVar()
        self.var.set(1)
        label_frame0 = LabelFrame(self, text="モード", height=50, width=200)
        label_frame0.place(x=15,y=20)
        r_button1 = Radiobutton(self, text="自動", variable=self.var, value=1)
        r_button1.place(x=20,y=40)
        r_button2 = Radiobutton(self, text="手動", variable=self.var, value=2)
        r_button2.place(x=120,y=40)
        
        
        label_frame1 = LabelFrame(self, text='出品時間の間隔', height=50, width=200)
        label_frame1.place(x=15,y=85)
        self.E1 = Entry(self, bd=1)
        self.E1.insert(0, 20)
        self.E1.place(x=20,y=105,width=50)
        text1 = Label(self, text="分から")
        text1.place(x=70,y=105)
        self.E2 = Entry(self, bd=1)
        self.E2.insert(0, 35)
        self.E2.place(x=140,y=105,width=50)
        text2 = Label(self, text="分")
        text2.place(x=190,y=105)
        
        label_frame2 = LabelFrame(self, text='ツール稼働時間', height=80, width=200)
        label_frame2.place(x=15,y=150)
        # cal1 = DateEntry(self, bd=1)
        # cal1.place(x=20,y=200)
        self.start_time = Entry(self, bd=1)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.start_time.insert(0, current_time)
        self.start_time.place(x=20,y=170,width=130)
        text4 = Label(self, text="開始時間")
        text4.place(x=150,y=170)
        self.end_time = Entry(self, bd=1)
        prevent_time = (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")
        self.end_time.insert(0, prevent_time)
        self.end_time.place(x=20,y=200,width=130)
        text5 = Label(self, text="終了時間")
        text5.place(x=150,y=200)
        
        self.var1 = IntVar()
        self.var1.set(0)
        # label_frame0 = LabelFrame(self, text="モード", height=50, width=200)
        # label_frame0.place(x=15,y=20)
        r_button1 = Radiobutton(self, text="今すぐ開始", variable=self.var1, value=1, command=self.activation)
        r_button1.place(x=20,y=240)
        r_button2 = Radiobutton(self, text="時間を指定", variable=self.var1, value=2, command=self.activation)
        r_button2.place(x=120,y=240)
        
        # create button, link it to clickExitButton()
        start_button = Button(self, text="開始", command=self.clickStartButton)
        start_button.place(x=20, y=275, width=80)
        close_button = Button(self, text="完了", command=self.clickExitButton)
        close_button.place(x=130, y=275, width=80)
    
    def activation(self):
        if self.var1.get() == 1:
            self.start_time.config(state="disabled")
            self.end_time.config(state="disabled")
        else:
            self.start_time.config(state="normal")
            self.end_time.config(state="normal")
        
    def clickStartButton(self):
        end_time = self.end_time.get()
        end_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        if self.var1.get() == 2:
            start_time = self.start_time.get()
            start_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            while True:
                current_obj = datetime.now()
                print(f"waiting...      {current_obj}")
                if (current_obj >= start_obj):
                    if start_obj <= end_obj:
                        break
                    else:
                        messagebox.showinfo("アラート", "稼働時間を正しく入力してください！")
                        break
        username = "i-hirose@k-andi.co.jp"
        password = "Ez9ubrcG"
        
        # Go to site
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome()
        statusbar.config(text="稼働を開始しました。")
        app.update()
        driver.get('https://gameclub.jp')

        # Press the sell button
        sell_button = driver.find_element("xpath", "//i[@class='fas fa-camera']")
        sell_button.click()

        statusbar.config(text="ログイン中です…")
        app.update()
        # Input email and password
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(username)
        time.sleep(2)
        pwd_input = driver.find_element(By.NAME, "password")
        pwd_input.send_keys(password)
        time.sleep(2)

        # Click the captcha button
        recaptcha = driver.find_element(By.XPATH, "//div[@class = 'g-recaptcha']")
        recaptcha.click()
        time.sleep(10)

        #Judge the status of check
        driver.switch_to.default_content()
        check_status = driver.find_element(By.XPATH, "//div[5]")
        status = check_status.value_of_css_property("visibility")
        print(status)

        if status != "hidden":
            statusbar.config(text="Captcha認証の突破中です…")
            app.update()
            # Get audio challenge
            driver.switch_to.default_content()
            frames=driver.find_element(By.XPATH, "//div[5]").find_elements(By.TAG_NAME, "iframe")
            driver.switch_to.frame(frames[0])
            driver.find_element(By.ID, "recaptcha-audio-button").click()

            # Click the play button
            driver.switch_to.default_content()   
            frames= driver.find_elements(By.TAG_NAME, "iframe")
            driver.switch_to.frame(frames[-1])
            time.sleep(2)
            driver.find_element(By.XPATH, "//div/div//div[3]/div/button").click()

            #get the mp3 audio file
            src = driver.find_element(By.ID, "audio-source").get_attribute("src")
            print("[INFO] Audio src: %s"%src)   

            #download the mp3 audio file from the source
            file_path = os.path.join(os.getcwd(), "captcha.wav")
            print(file_path)
            urllib.request.urlretrieve(src, file_path)

            data,samplerate=soundfile.read('captcha.wav')
            soundfile.write('new.wav',data,samplerate, subtype='PCM_16')
            r=sr.Recognizer()
            with sr.AudioFile("new.wav") as source:
                audio_data=r.record(source)
                text=r.recognize_google(audio_data)
                print(text)

            # Click the verify button
            driver.find_element(By.ID, "audio-response").send_keys(text)
            driver.find_element(By.ID, "recaptcha-verify-button").click()

        time.sleep(3) 

        driver.switch_to.default_content()
        login_click = driver.find_element(By.XPATH,"//button[@class='btn btn-danger btn-registration']")
        login_click.click()

        statusbar.config(text="ログインが完了しました。")
        app.update()
        time.sleep(3)
        
        index = 0
        flag = True
        while flag:
            time.sleep(4)
            end_time = self.end_time.get()
            end_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            current_obj = datetime.now()
            if current_obj >= end_obj:
                flag = False
                print("The tool is closed")
                break
            
            googlesheetid='1uXXG0LjOf6xIr3mqimVH6Kcwkj-tYZ_oLOpgYlQJAnA'
            sheetname='Gameclub.jp'
            url=f"https://docs.google.com/spreadsheets/d/{googlesheetid}/gviz/tq?tqx=out:csv&sheet={sheetname}"
            content=pd.read_csv(url)
            
            # mode setting
            if self.var.get() == 1:
                check_status = True
            else:
                check_status = content.iloc[index, 0]
            
            # exhibit only when the check is activated   
            if not check_status:
                index += 1
                continue
            
            if math.isnan(content.iloc[index, 1]):
                index = 0
                continue
            
            # index = 0
            statusbar.config(text="出品中です…")
            app.update()
            # upload_Image = content.iloc[index,2]
            upload_Image = r"F:\image\logo\circula.png"
            driver.find_element(By.XPATH, "//input[@type='file']").send_keys(upload_Image)
            
            search = driver.find_element(By.ID, "btn-search-title")
            search.click()
            
            time.sleep(10)
            
            search_title = driver.find_element(By.ID, "search-title-input")
            search_title.send_keys(content.iloc[index,3])

            time.sleep(5)
            item = driver.find_element(By.XPATH, "//div[@class='item']")
            item.click()

            time.sleep(3)

            if content.iloc[index,4] == "代行":
                radio = driver.find_element(By.ID, "account-type-id-40")
            else:
                radio = driver.find_element(By.ID, "account-type-id-10")
            radio.click()

            name = driver.find_element(By.NAME, "name")
            name.send_keys(content.iloc[index,5])

            detail = driver.find_element(By.NAME, "detail")
            detail.send_keys(content.iloc[index,6])
            
            if not math.isnan(content.iloc[index, 7]):
                member = driver.find_element(By.NAME, "subcategory_unique_property_1_value")
                member.send_keys(int(content.iloc[index, 7]))
            
            if not math.isnan(content.iloc[index, 8]):
                circle = driver.find_element(By.NAME, "subcategory_unique_property_2_value")
                circle.send_keys(int(content.iloc[index, 8]))

            if not math.isnan(content.iloc[index, 9]):
                retry_time = driver.find_element(By.NAME, "subcategory_unique_property_3_value")
                retry_time.send_keys(int(content.iloc[index, 9]))

            if not math.isnan(content.iloc[index, 10]):
                rate = driver.find_element(By.NAME, "subcategory_unique_property_4_value")
                rate.send_keys(int(content.iloc[index, 10]))

            if not isinstance(content.iloc[index, 11], (int, float)):
                notice = driver.find_element(By.NAME, "notice_information")
                notice.send_keys(content.iloc[index,11])

            price_budget = int(content.iloc[index, 12])
            price = driver.find_element(By.NAME, "price")
            price.send_keys(price_budget)

            confirm_button = driver.find_element(By.ID, "btn-confirm")
            confirm_button.click()

            time.sleep(2)
            add_button = driver.find_element(By.ID, "btn-add")
            add_button.click()
            statusbar.config(text="出品が完了しました。", fg="green")
            app.update()
            time.sleep(3)
            close_button = driver.find_element(By.XPATH, "//*[@id='content-wrapper']/div/div[2]/div[8]/div/div[1]/i")
            close_button.click()
            
            current_obj = datetime.now()
            if current_obj >= end_obj:
                flag = False
                print("The tool is closed")
                break

            time1 = int(self.E1.get()) * 60
            time2 = int(self.E2.get()) * 60
            wait_time = random.uniform(time1, time2)
            print(wait_time)
            
            current_obj = datetime.now()
            wait_delta = timedelta(seconds=wait_time)
            if (current_obj+wait_delta) >= end_obj:
                flag = False
                print("The tool is closed")
                break
            
            statusbar.config(text="待機中です…")
            app.update()
            time.sleep(wait_time)
            
            return_button = driver.find_element(By.XPATH, "//*[@id='content-wrapper']/header/div/div[2]/div[2]/a[2]")
            return_button.click()
            index = index + 1
            print(index)
        # driver.quit()

    def clickExitButton(self):
        exit()

root = Tk()
app = Window(root)
statusbar = Label(app, text="設定してください。", bd=1, relief=SUNKEN, anchor=E)
statusbar.pack(side=BOTTOM, fill=X)
root.wm_title("gameclub.jp")
root.geometry("230x330+1100+400")
root.resizable(False, False)
root.mainloop()