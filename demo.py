from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from data_testing.get_values import football_values
from frame_testing.ui_main import HelloFrame
import wx
from selenium.webdriver.chrome.options import Options
import threading

service = Service(r'C:/webdrivers/chromedriver.exe')
service.start()

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options, executable_path=r'C:/webdrivers/chromedriver.exe')



def HTG_compare(score):
    hometeam = int(score[0])
    awayteam = int(score[1])

    if hometeam > awayteam:
        if (hometeam - awayteam) == 1:
            return (football_values[0])
            
        elif (hometeam - awayteam) == 2:
            return (football_values[0] * 1.2)
            
        elif (hometeam - awayteam) == 3:
            return (football_values[0] * 1.5)
            
        else:
            return (football_values[0] * 2)      
    
    elif awayteam > hometeam:
        if (awayteam - hometeam) == 1:
            return -(football_values[0])
            
        elif (awayteam - hometeam) == 2:
            return -(football_values[0] * 1.2)
            
        elif (awayteam - hometeam) == 3:
            return -(football_values[0] * 1.5)
            
        else:
            return -(football_values[0] * 2)

    elif hometeam == awayteam:
        return 0
    
    else:
        print("Error")

def S_compare(value):
    hometeam = (int(value['Shots on Goal'][0]) + int(value["Shots off Goal"][0]))
    awayteam = (int(value['Shots on Goal'][1]) + int(value["Shots off Goal"][1]))

    if hometeam > awayteam:
        if (hometeam - awayteam) < 3:
            return (football_values[1])
            
        elif (hometeam - awayteam) < 5:
            return (football_values[1] * 1.2)
            
        elif (hometeam - awayteam) < 7:
            return (football_values[1] * 1.5)
            
        else:
            return (football_values[1])    
    
    elif awayteam > hometeam:
        if (awayteam - hometeam) < 3:
            return -(football_values[1])
            
        elif (awayteam - hometeam) < 5:
            return -(football_values[1] * 1.2)
            
        elif (awayteam - hometeam) < 7:
            return -(football_values[1] * 1.5)
            
        else:
            return -(football_values[1] * 2)

    elif hometeam == awayteam:
        return 0
    
    else:
        print("Error")

def ST_compare(value):
    hometeam = int(value['Shots on Goal'][0])
    awayteam = int(value['Shots on Goal'][1])

    if hometeam > awayteam:
        if (hometeam - awayteam) < 3:
            return (football_values[2])
            
        elif (hometeam - awayteam) < 5:
            return (football_values[2] * 1.2)
            
        elif (hometeam - awayteam) < 7:
            return (football_values[2] * 1.5)
            
        else:
            return (football_values[2] * 2)      
    
    elif awayteam > hometeam:
        if (awayteam - hometeam) < 3:
            return -(football_values[2])
            
        elif (awayteam - hometeam) < 5:
            return -(football_values[2] * 1.2)
            
        elif (awayteam - hometeam) < 7:
            return -(football_values[2] * 1.5)
            
        else:
            return -(football_values[2] * 2)

    elif hometeam == awayteam:
        return 0
    
    else:
        print("Error")

def Y_compare(value):
    hometeam = int(value['Yellow Cards'][0]) 
    awayteam = int(value['Yellow Cards'][1])


    if hometeam > awayteam:
        if (hometeam - awayteam) < 3:
            return -(football_values[3])
            
        elif (hometeam - awayteam) < 5:
            return -(football_values[3] * 1.2)
            
        elif (hometeam - awayteam) < 7:
            return -(football_values[3] * 1.5)
            
        else:
            return -(football_values[3])      
    
    elif awayteam > hometeam:
        if (awayteam - hometeam) < 3:
            return (football_values[3])
            
        elif (awayteam - hometeam) < 5:
            return (football_values[3] * 1.2)
            
        elif (awayteam - hometeam) < 7:
            return (football_values[3] * 1.5)
            
        else:
            return (football_values[3] * 2)

    elif hometeam == awayteam:
        return 0
    
    else:
        print("Error")
    


def R_compare(value):
    try:
        hometeam = int(value['Red Cards'][0]) 
    except:
        hometeam = 0
    
    try:
        awayteam = int(value['Red Cards'][0])
    except:
        awayteam = 0 


    if hometeam > awayteam:
        if (hometeam - awayteam) < 2:
            return -(football_values[4])
            
        elif (hometeam - awayteam) < 3:
            return -(football_values[4] * 1.2)
            
        elif (hometeam - awayteam) < 4:
            return -(football_values[4] * 1.5)
            
        else:
            return -(football_values[4] * 2)     
    
    elif awayteam > hometeam:
        if (awayteam - hometeam) < 2:
            return (football_values[4])
            
        elif (awayteam - hometeam) < 3:
            return (football_values[4] * 1.2)
            
        elif (awayteam - hometeam) < 4:
            return (football_values[4] * 1.5)
            
        else:
            return (football_values[4] * 2)

    elif hometeam == awayteam:
        return 0
    
    else:
        print("Error")
    
def winning_team(team_score):

    if team_score > 0:
        return " You should bet for H"
    elif team_score < 0:
        return " You should bet for A"
    else:
        return " You should bet for D"

def get_stats(matches):
    info_stat = []
    
    for match in matches:
        match_url = "https://www.flashscore.com/match/" + match[4:] + "/#match-summary"
        print(match_url)
        driver.get(match_url)
        
        time.sleep(3)
        driver.find_element_by_xpath("""//*[@id="li-match-statistics"]""").click()
        time.sleep(1)
        
        info_raw = driver.find_elements_by_class_name("statText.statText")
        standings_raw = driver.find_elements_by_class_name("current-result").text
        print(standings_raw)
        info = []
        for element in info_raw:
            info.append(element.text)
        
        driver.implicitly_wait(3)
        info = remove_values_from_list(info, '')
        
        info_stat.append(info)
        time.sleep(2)
    driver.quit()
    return info_stat

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def get_matches():
    driver.get("https://www.flashscore.com/")


    _ = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, """//*[@id="live-table"]/div[1]/div/div[2]""")))
    driver.find_element_by_xpath("""//*[@id="live-table"]/div[1]/div/div[2]""").click()


    _ = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "container__fsbody")))
    

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    matches_raw = soup.find_all('div', class_='event__match' )
    match_id = []
    for tag in matches_raw:
        match_id.append(tag.get("id"))
    
    return match_id
    


def get_stats1(match):
    
   
    
    match_url = "https://www.flashscore.com/match/" + match[4:] + "/#match-summary"
    driver.get(match_url)
    
    element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, """//*[@id="li-match-statistics"]""")))

    element.click()
    
    element = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "current-result")))
    standings_raw = driver.find_elements_by_class_name("current-result") 

    element = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "statText.statText")))
    info_raw = driver.find_elements_by_class_name("statText.statText")
    
    standings = []
    for char in standings_raw:
        standings.append(char.text)
    info = []
    for element in info_raw:
        info.append(element.text)
        
    
    info = remove_values_from_list(info, '')
    

    
    return(info, standings, match_url)

 

def list_to_string(s):  
    
    str1 = ""  
       
    for ele in s:  
        str1 += ele   
       
    return str1

def list_to_string_spaces(list):
    info_string = ""
    for line in list:
        info_string += str(line)
        info_string += "\n"
    return info_string


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title)

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.gauge = wx.Gauge(panel, -1, 10, size=(250, 25))
        self.btn1 = wx.Button(panel, wx.ID_OK, label="Start")
        self.btn2 = wx.Button(panel, wx.ID_STOP, label="Cancel")
        self.text = wx.StaticText(panel, -1, "Click start to run web scraping")
        
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnStop, self.btn2)

        hbox1.Add(self.gauge, 1, wx.ALIGN_CENTRE)
        hbox2.Add(self.btn1, 1, wx.RIGHT, 10)
        hbox2.Add(self.btn2, 1)
        hbox3.Add(self.text, 1)
        
        vbox.Add((0, 50), 0)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 30), 0)
        vbox.Add(hbox2, 1, wx.ALIGN_CENTRE)
        vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)

        panel.SetSizer(vbox)
        self.Centre()

    def OnOk(self, event):
        self.text.SetLabel("Gathering live matches")
        self.gauge.UpdateWindowUI()
        ex.Yield()

        app = wx.App()
        frm = HelloFrame(None, title='Betting predictions')

        #ex = wx.App()

        results = []

        matches1 = ["eeeez7bKeorA", "eeeeU5iTgPCM", "eeeeSteCc7Dc", "eeeedGaGdRS3", "eeeeQywal3zp", "eeeeIVmPf5cG"] #Set of old matches for demo version
        try:
            matches = get_matches() #Will not be used in demo version due to no live matches
            
            self.gauge.SetRange(len(matches1) + 3) #Should be matches in full version
        
        except:
            matches = get_matches() #Will not be used in demo version due to no live matches
            
            self.gauge.SetRange(len(matches1) + 3) #Should be matches in full version
        
        finally:
            value = 3
            self.gauge.SetValue(value)
            self.gauge.UpdateWindowUI()
            ex.Yield()

            self.text.SetLabel("Gathering stats from matches")
            self.gauge.UpdateWindowUI()
            ex.Yield()

            for match in matches1: #Should be matches once matches are live again
                
                try:
                    stat_input, standings_unprocessed, url = get_stats1(match) 

                except:
                    stat_input, standings_unprocessed, url = get_stats1(match) 

                finally:
                    standings = []
                    standings_unprocessed = list_to_string(standings_unprocessed)
                    standings.append(standings_unprocessed[0])
                    standings.append(standings_unprocessed[3])
                    match_stat = {}
                    
                    for _ in range(int(len(stat_input) / 3)):
                        match_stat[stat_input[1]] = [stat_input[0], stat_input[2]]
                        stat_input = stat_input[3:]
                        
                    team_performance_score = HTG_compare(standings)
                    team_performance_score += ST_compare(match_stat)
                    team_performance_score += S_compare(match_stat)
                    team_performance_score += Y_compare(match_stat)
                    team_performance_score += R_compare(match_stat)
                    
                    prediction = winning_team(team_performance_score)
                    
                    text = str("In match with url " + url + prediction)    
                    results.append(text)
                    
                    value = value + 1
                    self.gauge.SetValue(value)
                    self.gauge.UpdateWindowUI()
                    ex.Yield()

                        
            driver.quit()
            results = list_to_string_spaces(results)
            
            self.text.SetLabel("Calculations finished")
            self.gauge.UpdateWindowUI()
            ex.Yield()
            time.sleep(1)
            
            frm.change_text(results)
            frm.message("Your predictions are ready, click OK to show")
            self.Close()

            frm.Show()
            app.MainLoop()

    def OnStop(self, event):
        self.text.SetLabel("Task Interrupted")
        self.Close()
        #app = wx.App() #Dummy does not do anything just to allow a message
        #frm = HelloFrame(None, title='Betting app') #Dummy does not do anything just to allow a message
        #frm.message("Task failed successfully! \n \n Why did you click this? Well, now the program is broken so you might as well restart")

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Betting app")
        frame.Show(True)
        return True

if __name__ == "__main__":
    ex = MyApp(0)
    ex.MainLoop()