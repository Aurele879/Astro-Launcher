import os
import customtkinter
from tkinter import PhotoImage, Label, messagebox
from PIL import Image, ImageTk
import minecraft_launcher_lib
import subprocess
import threading
import configparser
import uuid
import requests
from zipfile import ZipFile
from time import sleep

#Data
config = configparser.ConfigParser()
config_file = config.read('saved.ini')
last_played_version = config['DATA'].get('last_played')



#Game Vars
minecraft_directory = os.path.join(os.path.expanduser("~"), "AppData\\Roaming\\.astrolauncher")
if os.path.isdir(minecraft_directory):
    pass
else:
    os.mkdir(minecraft_directory)
    os.mkdir(os.path.join(minecraft_directory, "versions"))

brut_installed_version_list = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)
installed_version_list = []
for element in brut_installed_version_list:
    installed_version_list.append(element["id"])

brut_official_version_list = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
official_version_list = []
for element in brut_official_version_list:
    if element["type"] == "release":
        official_version_list.append(element["id"])


special_official_version_list = []
for element in brut_official_version_list:
    special_official_version_list.append(element["id"])

final_version_list = ["Latest"] + official_version_list
for element in installed_version_list:
    if element in final_version_list:
        pass
    else:
        final_version_list.append(element)

final_special_version_list = ["Latest"]+ special_official_version_list
for element in installed_version_list:
    if element in final_special_version_list:
        pass
    else:
        final_special_version_list.append(element)

if config['SETTINGS'].get('special_versions') == "on":
    version_list = final_special_version_list
else:
    version_list = final_version_list



#Fucntions
def check_jre(version):
    for element in ['1.16.5', '1.16.4', '1.16.3', '1.16.2', '1.16.1', '1.16', '1.15.2', '1.15.1', '1.15', '1.14.4', '1.14.3', '1.14.2', '1.14.1', '1.14', '1.13.2', '1.13.1', '1.13', '1.12.2', '1.12.1', '1.12', '1.11.2', '1.11.1', '1.11', '1.10.2', '1.10.1', '1.10', '1.9.4', '1.9.3', '1.9.2', '1.9.1', '1.9', '1.8.9', '1.8.8', '1.8.7', '1.8.6', '1.8.5', '1.8.4', '1.8.3', '1.8.2', '1.8.1', '1.8', '1.7.10', '1.7.9', '1.7.8', '1.7.7', '1.7.6', '1.7.5', '1.7.4', '1.7.3', '1.7.2', '1.6.4', '1.6.2', '1.6.1', '1.5.2', '1.5.1', '1.4.7', '1.4.5', '1.4.6', '1.4.4', '1.4.2', '1.3.2', '1.3.1', '1.2.5', '1.2.4', '1.2.3', '1.2.2', '1.2.1', '1.1', '1.0']:
        if version in element:
            return "legacy"

    for element in ['1.20.4', '1.20.3', '1.20.2', '1.20.1', '1.20', '1.19.4', '1.19.3', '1.19.2', '1.19.1', '1.19', '1.18.2', '1.18.1', '1.18', '1.17.1', '1.17']:
        if version in element:
            return "17"
             
    for element in ['1.20.6', '1.20.5']:
        if version in element:
            return "21"
        else:
            return "21"
        
def install_jdk21():
    if os.path.isdir("jdk-21.0.3"):
        print("ALREADY DONE")
    else:
        info_label.configure(text="Downloading Java Development Kit 21...")
        url = "https://www.dropbox.com/scl/fi/f06eq358jri68bi3zch9a/jdk-21_windows-x64_bin.zip?rlkey=cbld4fzyncabxu4ycq0tz7qzf&st=by6t5vce&dl=1"
        r = requests.get(url, allow_redirects=True)
        info_label.configure(text="Exctracting java files ...")
        with open("jdk-21_windows-x64_bin.zip", 'wb') as f:
            f.write(r.content)
        with ZipFile("jdk-21_windows-x64_bin.zip", 'r') as zip: 
            zip.printdir() 
            zip.extractall() 
        info_label.configure(text="Java Development Kit 21 is installed !")
        os.remove("jdk-21_windows-x64_bin.zip")
    info_label.forget()

def install_jdk17():
    if os.path.isdir("jdk-17.0.11"):
        print("ALREADY DONE")
    else:
        info_label.configure(text="Downloading Java Development Kit 17 ...")
        url = "https://www.dropbox.com/scl/fi/w28ti70pius6fwktpojot/jdk-17_windows-x64_bin.zip?rlkey=40erwi7l60vuoa083ws85zost&st=tcivifum&dl=1"
        r = requests.get(url, allow_redirects=True)
        info_label.configure(text="Exctracting java files ...")
        with open("jdk-17_windows-x64_bin", 'wb') as f:
            f.write(r.content)
        with ZipFile("jdk-17_windows-x64_bin", 'r') as zip: 
            zip.printdir() 
            zip.extractall() 
        info_label.configure(text="Java Development Kit 17 is installed !")
        os.remove("jdk-17_windows-x64_bin")
    info_label.forget()

def install_jre8():
    if os.path.isdir("jre-8"):
        print("ALREADY DONE")
    else:
        info_label.configure(text="Downloading Java 8...")
        url = "https://www.dropbox.com/scl/fi/eexnxjq7x5my45kx69tfg/jre-legacy.zip?rlkey=8a9pzpd1yt0fpvhyh24vxkamw&dl=1"
        r = requests.get(url, allow_redirects=True)
        info_label.configure(text="Exctracting java files ...")
        with open("jre-legacy.zip", 'wb') as f:
            f.write(r.content)
        with ZipFile("jre-legacy.zip", 'r') as zip: 
            zip.printdir() 
            zip.extractall() 
        info_label.configure(text="Java 8 is installed !")
        os.remove("jre-legacy.zip")
    info_label.forget()

def hide_ui():
    combobox.place_forget()
    play_button.place_forget()
    settings_button.place_forget()
    entry_nickname.place_forget()
    more_version_button.place_forget()
    print("Hiding UI")


def show_ui():
    play_button.place(x=750, y=470)
    settings_button.place(x=670, y=470)
    combobox.place(x=50, y=460)
    entry_nickname.place(x=50, y=500)
    more_version_button.place(x=204, y=460)
    print("Showing UI")


def loading_page():
    print("Loading UI")
    hide_ui()
    loading_bar = customtkinter.CTkProgressBar(root,
                                                mode="indeterminate",
                                                  width=660, height=20,
                                                    corner_radius=100,
                                                      fg_color="#474747",
                                                        bg_color="#1E1E1E",
                                                          progress_color="#47316F")
    loading_bar.place(x=50, y=485)
    loading_bar.start()
    info_label.place(x=55, y=510)

    cancel_button = customtkinter.CTkButton(root,
                                             command=stop,
                                               fg_color="#47316F",
                                                 bg_color="#1E1E1E",
                                                   hover_color="#342451",
                                                     text="CANCEL",
                                                       width=200,
                                                         height=50,
                                                           corner_radius=20,
                                                             font=("Arial", 25, "bold"))
    cancel_button.place(x=750, y=470)


def settings_btn():
    print("Opening settings")
    hide_ui()
    settings = customtkinter.CTk()

    def close_settings():
        settings.destroy()
        show_ui()
        print("Closing settings")

    def save_settings():
        print("Saving settings")
        if entry_java_path.get() == "" or entry_java_path.get() == " " or entry_java_path.get() == None:
            pass
        else:
            config.set('SETTINGS', 'java_path', entry_java_path.get())
        config.set('SETTINGS','special_versions', special_versions_button.get())
        with open('saved.ini', 'w') as fichier_config:
            config.write(fichier_config)
        close_settings()

    settings.attributes('-topmost', 1)
    settings.after(100, lambda: settings.attributes('-topmost', 1))
    settings.geometry("600x400")
    settings.title("Settings")
    settings.configure(fg_color="#1E1E1E")
    settings.protocol("WM_DELETE_WINDOW", close_settings)
    settings.resizable(False, False)
    settings.iconbitmap("assets/icon.ico")

    titre = Label(settings, text="Choose your preferences", font=("Arial", 20, "bold"), fg="#FFFFFF", bg="#1E1E1E")
    titre.place(x=135, y=20)
    
    java_label = Label(settings, text="Java path (keep empty to use default version): ", font=("Arial", 10, "italic"), fg="#FFFFFF", bg="#1E1E1E")
    java_label.place(x=20, y=95)

    entry_java_path = customtkinter.CTkEntry(settings, width=560, height=30, fg_color="#707070")
    entry_java_path.place(x=20, y=120)
    entry_java_path.insert(0, config['SETTINGS'].get('java_path'))

    save_button = customtkinter.CTkButton(settings, text="SAVE", command=save_settings, fg_color="#47316F", hover_color="#342451", font=("Arial", 13, "bold"))
    save_button.place(x=450, y=350)

    quit_button = customtkinter.CTkButton(settings, text="CANCEL", command=close_settings, fg_color="#47316F", hover_color="#342451", font=("Arial", 13, "bold"))
    quit_button.place(x=300, y=350)

    switch_var = customtkinter.StringVar(value=config['SETTINGS'].get('special_versions'))
    special_versions_button = customtkinter.CTkSwitch(settings,
                                                       text="Enable special versions (restart the game to change)",
                                                         text_color="white",
                                                           fg_color="gray",
                                                             progress_color="red",
                                                               variable=switch_var,
                                                                 onvalue="on",
                                                                   offvalue="off")
    special_versions_button.place(x=20, y=160)

    settings.mainloop()


def launch_selected_version():
    info_label.configure(text="Downloading game files ...")
    version = combobox_var.get()
    if version == "Latest":
        version = minecraft_launcher_lib.utils.get_latest_version()["release"]
    config.set('DATA', 'last_played', version)
    with open('saved.ini', 'w') as fichier_config:
        config.write(fichier_config)
    if version not in installed_version_list:
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)
    if config['SETTINGS'].get('java_path') == "default":
        if check_jre(version=version) == "legacy":
            install_jre8()
            jpath = "jre-8/bin/javaw.exe"
        elif check_jre(version=version) == "17":
            install_jdk17()
            jpath = "jdk-17.0.11/bin/javaw.exe"
        elif check_jre(version=version) == "21":
            install_jdk21()
            jpath = "jdk-21.0.3/bin/javaw.exe"
            
    else:
        jpath = config['SETTINGS'].get('javapath')

    options = {"username": config['SETTINGS'].get('nickname'),
               "uuid": str(uuid.uuid4()),
               "token": "",
               "executablePath": jpath}
    info_label.configure(text="Launching game ...")
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
    root.withdraw()
    subprocess.run(minecraft_command)
    os._exit(1)

def stop():
    print("Canceling")
    os._exit(1)

def play_btn():
    loading_page()
    config.set('SETTINGS','nickname', entry_nickname.get())
    with open('saved.ini', 'w') as fichier_config:
        config.write(fichier_config)
    threading.Thread(target=launch_selected_version).start()


def modloaders():
  messagebox.showwarning(title="Warning",message="Installing Modloaders is not a supported feature, this means the game can crash if you are installing one. However, you can try, like we say in french : << Sur un malentendu ça peut passer ! >>")



#GUI
root = customtkinter.CTk()
root.geometry("1000x550")
root.title("Astro Minecraft Launcher")
root.resizable(False, False)

gear = Image.open("assets/gear.png")
arrow = Image.open("assets/arrow.png")
root.iconbitmap("assets/icon.ico")

bg_img= PhotoImage(file = "assets/background.png")
bg= Label(root, image = bg_img)
bg.pack()

info_label = customtkinter.CTkLabel(root, text="", text_color="white", bg_color="#1E1E1E", font=("Arial", 15, "bold"))

play_button = customtkinter.CTkButton(root, command=play_btn,
                                       fg_color="#47316F",
                                         bg_color="#1E1E1E",
                                           hover_color="#342451",
                                             text="PLAY",
                                               width=200,
                                                 height=50,
                                                   corner_radius=20,
                                                     font=("Arial", 25, "bold"))
play_button.place(x=750, y=470)

settings_button = customtkinter.CTkButton(root,
                                           command=settings_btn,
                                             image=customtkinter.CTkImage(gear, size=(30, 30)),
                                               fg_color="#47316F",
                                                 bg_color="#1E1E1E",
                                                   hover_color="#342451",
                                                     text="",
                                                       width=50,
                                                         height=50,
                                                           corner_radius=20)
settings_button.place(x=670, y=470)

more_version_button = customtkinter.CTkButton(root,
                                           command=modloaders,
                                               fg_color="#47316F",
                                                 bg_color="#1E1E1E",
                                                   hover_color="#342451",
                                                     text="+",
                                                       width=46,
                                                         height=28,
                                                           corner_radius=100)
more_version_button.place(x=204, y=460)

combobox_var = customtkinter.StringVar()
combobox = customtkinter.CTkComboBox(root, values=version_list, variable=combobox_var, bg_color="#1E1E1E", fg_color="#47316F", button_color="#47316F", border_color="#47316F", text_color="white", state="readonly", corner_radius=15, width=150)
combobox_var.set(last_played_version)
combobox.place(x=50, y=460)

entry_nickname = customtkinter.CTkEntry(root, height=26, placeholder_text="Nickname", placeholder_text_color="gray",  bg_color="#1E1E1E", fg_color="white", border_color="white", text_color="black", corner_radius=15, width=200)
entry_nickname.place(x=50, y=500)
if config['SETTINGS'].get('nickname') != "":
    entry_nickname.insert(0, config['SETTINGS'].get('nickname'))

root.protocol("WM_DELETE_WINDOW", stop)
root.mainloop()



#NOTICE#

#EN#
#This software was designed by Øré, it certainly has some bugs, please post them on github so I can improve the software, enjoy!
#All the code here is free and I encourage you to use it for your own projects.
#buildapp cmd : python buildapp.py build

#FR#
#Ce logiciel à été concu par Øré, il comporte certainement quelques bugs, merci de les poster sur github car cela me permettra de m'améliorer, bon jeu !
#Tout le code ici présent est libre de droit et je vous encorage à l'utiliser pour vos propres projets.
#buildapp cmd : python buildapp.py build