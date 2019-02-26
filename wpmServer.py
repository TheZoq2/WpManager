#!/bin/python
from multiprocessing import connection
import threading
import time
import subprocess

import Timer

def run_server():
    #Defining variables for configuration
    COMM_PORT = 6724 #The port the server and clients will use
    LOOP_UPDATE_RATE = 1; #The time to sleep for between loop updates.

    WALLPAPER_FOLDER = "/tmp/wallpaper/"
    WP_FILENAME = "out.png"



    class MainClass:
        def __init__(self, wallpaperPath):
            #The program should exit if this variable is false
            self.running = True
            self.wallpaperPath = wallpaperPath
            #Create a timer object

            self.timer = Timer.Timer(self.notifyWallpaper)

            #Start a separate thread which handles scheduled tasks, like timers
            self.updateThread = threading.Thread(target=self.updateLoop)
            self.updateThread.start()

            #Create a directory for storing changed wallpapers
            subprocess.call(["mkdir", "-p", WALLPAPER_FOLDER])

        def updateLoop(self):
            while self.running:
                time.sleep(LOOP_UPDATE_RATE)

                self.timer.update()

        def main(self):
            address = ("localhost", COMM_PORT)
            
            #Creating a listener that listens for commands
            listener = connection.Listener(address)
            
            while(self.running):
                #Wait for clients to connect
                conn = listener.accept();
            
                msg = conn.recv()
                print("Got msg: {}".format(msg))

                command = msg.split(".")

                if(command[0] == "kill"):
                    print("I die")
                    self.running = False

                elif command[0] == "timer":
                    if "=" in command[1]:
                        subCmd = command[1].split("=")

                        if subCmd[0] == "start":
                            print("Starting timer")
                            self.timer.start(int(subCmd[1]))
                    else:
                        if(command[1] == "reset"):
                            self.resetWallpaper()
                            print("Resetting wallpaper")
                        if command[1] == "check":
                            conn.send(str(self.timer.getTimeLeft()))
                else:
                    conn.send("Unknown command")


        def onTimerEnd(self):
            print("timer done")

        def notifyWallpaper(self):
            subprocess.call(["convert", self.wallpaperPath, "-fill", "red", "-colorize", "25", WALLPAPER_FOLDER + WP_FILENAME])
            subprocess.call(["feh", "--bg-fill", WALLPAPER_FOLDER + WP_FILENAME])

        def resetWallpaper(self):
            subprocess.call(["feh", "--bg-fill", self.wallpaperPath])
            

    mc = MainClass("/home/frans/Pictures/wallpapers/current.png")
    mc.main()
    
if __name__ == "__main__":
    run_server()
