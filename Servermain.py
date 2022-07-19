import socket
import threading
import phonenumbers
import folium
from phonenumbers import geocoder
import geocoder as gc
import webbrowser
import os
import codecs
import ipaddress
from tkinter import *
from tkinter import messagebox as messagebox
import tkinter as tk
from opencage.geocoder import OpenCageGeocode
import re
class SocketServer:
    def __init__(self,master):
        self.root=master
        self.server_socket=None
        self.create_listening_server()
        self.submit=None
        selfphoneField=None
        self.ipField=None
        self.info=None
        self.phnum=""
        self.ipnum=None
        self.ip_entry=tk.StringVar()
        self.phone_entry=tk.StringVar()
        self.filename=None
        
        self.my_address=()
        self.my_map1=None
        
        self.myMap=None
        self.location=()
        self.files=None
        self.lat=None
        self.long=None
        self.html_template=None
        self.htmltemplate=None
        self.geocoder=None
        self.initialize_gui()
        
    def create_listening_server(self):
            self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            local_ip='127.0.0.1'
            local_port=10319
            self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.server_socket.bind((local_ip,local_port))
            self.server_socket.listen(5)
            print("listening for input")
            client,addr=self.server_socket.accept()
            print("Accepted a connection from %s:%s"%(client,addr))
            dataFromClient=client.recv(1024)
            print(dataFromClient.decode())
            client.send("connected to server".encode())

        
        
    def initialize_gui(self):
        self.root.title("SMARTPHONE TRACKER")
        self.root.resizable(0,0)
        self.ip_textfield()
        self.phone_no_textfield()
        self.submit_button()
        

    def ip_textfield(self):
        frame=Frame()
        Label(frame,text='IP Address: ',font=("Helvetica",16)).pack(side='left',padx=10)
        self.ipField=tk.Entry(frame,bd=5,textvariable=self.ip_entry)
        self.ipField.pack(side='right',padx=10)
        frame.pack(side='top')
        
        
    def phone_no_textfield(self):
        frame=Frame()
        Label(frame,text='Phone number: ',font=("Helvetica",16)).pack(side='left',anchor='w')
        self.phoneField=tk.Entry(frame,bd=5,textvariable=self.phone_entry)
        self.phoneField.pack(side='right',padx=10)
        frame.pack(side='top',anchor='ne')
        
    def submit_button(self):
        frame=Frame()
        self.submit=Button(frame,text='Submit',width=10,command=self.on_submit).pack(side='bottom')
        frame.pack()

    def on_submit(self):
           
           self.ipnum=self.ip_entry.get()                                       
           if self.ipnum != ' ' :
               
               self.info=gc.ip(self.ipnum)
               self.my_address=self.info.latlng                
               self.my_map1=folium.Map(location=self.my_address,zoom_start=12)
               folium.CircleMarker(location=self.my_address,
                                   radius=50).add_to((self.my_map1))
               folium.Marker(location=self.my_address,popup=self.my_address).add_to((self.my_map1))
               self.my_map1.save("my_map.html")
               self.f=codecs.open('my_map.html','r+','utf-8')
               self.htmltemplate=self.f.read()
               self.f.write(self.htmltemplate)
               self.f.close()
               self.filename='file:///'+os.getcwd()+'/'+'my_map.html'
               webbrowser.open_new_tab(self.filename)






           self.phnum = self.phone_entry.get()
           if self.phnum  != 0 :
               self.key="8f5c94c5ee5d4c4491c13b7f2644e893"
               self.Phonenumber=self.phnum
               self.phonenumber=phonenumbers.parse(self.Phonenumber,None)
               self.validation=phonenumbers.is_valid_number(self.phonenumber)
               if(self.validation):
                   self.yourlocation=geocoder.description_for_number(self.phonenumber,"en")
                   self.geocoder=OpenCageGeocode(self.key)
                   self.query=str(self.yourlocation)
                   self.results=self.geocoder.geocode(self.query)
                   self.lat=self.results[0]['geometry']['lat']
                   self.lng=self.results[0]['geometry']['lng']
                   self.myMap=folium.Map(location=[self.lat,self.lng],zoom_start=5)
                   folium.Marker([self.lat,self.lng],popup=self.yourlocation).add_to((self.myMap))
                   self.myMap.save("myLocation.html")
                   self.files=codecs.open('myLocation.html','r+','utf-8')
                   self.html_template=self.files.read()
                   self.files.write(self.html_template)
                   self.files.close()
                   self.filename='file:///'+os.getcwd()+'/'+'myLocation.html'
                   webbrowser.open_new_tab(self.filename)
                   
              
                 
   
      
    def on_close_window(self):
        
            self.root.destroy()
            self.server_socket.close()
            exit(0)

    

#main function        
if __name__ == "__main__":
    root=Tk()
    gui=SocketServer(root)
    root.protocol("WM_DELETE_WINDOW",gui.on_close_window)
    root.mainloop()
    
