import requests
import re
import sys
from datetime import datetime
import sqlite3
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String, PickleType, select
from sqlalchemy.ext.declarative import declarative_base
import pickle
import tkinter as tk
import json

def getData(name, Base, engine, tags):
    with open('synonyms.json') as f:
        d = json.load(f)
        if name in d.keys():
            name = d[name]
    urlName = "https://" + name
    site = requests.get(urlName)
    text = site.text
    pattern = re.compile(r'<((?!!)/?[a-zA-Z]*[\s]*)')
    tagsDict = {}
    for i in re.findall(pattern, text):
        if i in tagsDict:
            tagsDict[i] += 1
        else:
            tagsDict[i] = 1
    sumOfTags = 0
    for i in tagsDict:
        sumOfTags += tagsDict[i]
    f = open("logs.txt","a+")
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S")
    f.write(timestampStr + "\t" + name + "\n")
    f.close() 

    query = db.insert(tags).values(name=name, url = urlName, date = dateTimeObj, tags_dict = tagsDict) 
    # ResultProxy = engine.execute(query)
    engine.execute(query) 
    return tagsDict

def view(name, engine, tags):
    with open('synonyms.json') as f:
        d = json.load(f)
        if name in d.keys():
            name = d[name]
    query = db.select([tags]).where(tags.name==name)
    ResultProxy = engine.execute(query)
    ResultSet = ResultProxy.first()
    return ResultSet

def main ():
    engine = create_engine('sqlite:///database.db')
    Base = declarative_base()

    class tags(Base):
        __tablename__ = "tags"
        id = Column(Integer, primary_key=True)
        name = Column(String)  
        url = Column(String)  
        date = Column(Date)  
        tags_dict = Column(PickleType)  
      
        def __init__(self, name, url, date, tags_dict):
            self.name = name   
            self.url = url   
            self.date = date   
            self.tags_dict = tags_dict       
    
    Base.metadata.create_all(engine)
    
    if len(sys.argv) > 1:
        if (sys.argv[1] == "--view"):
            print(view(sys.argv[2], engine, tags))
        elif (sys.argv[1] == "--get"):
            print(getData(sys.argv[2], Base, engine, tags))
    else:

        class App(tk.Frame):
            def __init__(self, master=None):
                super().__init__(master)
                self.master = master
                self.pack()
                self.create_widgets()


        
            def print_contents(self, event):
                print(self.contents.get())
        
            def create_widgets(self):
                self.get = tk.Button(self)
                self.get["text"] = "Загрузить"
                self.get["command"] = self.getDataW
                self.get.pack(side="left", pady=10)

                self.view = tk.Button(self)
                self.view["text"] = "Показать из базы"
                self.view["command"] = self.viewDataW
                self.view.pack(side="left", pady=10)

                self.entrythingy = tk.Entry()
                self.entrythingy.pack(side="top")
                self.contents = tk.StringVar()
                self.contents.set("")
                self.entrythingy["textvariable"] = self.contents
                self.entrythingy.bind('<Key-Return>',
                                      self.print_contents)

                self.get1 = tk.Button(self)
                self.get1["text"] = "Загрузить - Combobox"
                self.get1["command"] = self.getDataS
                self.get1.pack(side="left", pady=10)

                self.view1 = tk.Button(self)
                self.view1["text"] = "Показать из базы - Combobox"
                self.view1["command"] = self.viewDataS
                self.view1.pack(side="left", pady=10)

                
                self.Lb1 = tk.Listbox(root)
                self.Lb1.pack(side="top")
                self.Lb1.insert(1, "google.com")
                self.Lb1.insert(2, "www.facebook.com")
                self.Lb1.pack()

        
            def getDataW(self):
                DataForDisplay = getData(self.contents.get(), Base, engine, tags)
                text.set(DataForDisplay)
                app.delete('1.0', tk.END)
                app.insert(tk.CURRENT, text.get())
                app.mainloop()
                

            def viewDataW(self):
                DataForDisplay = view(self.contents.get(), engine, tags)
                text.set(DataForDisplay)
                app.delete('1.0', tk.END)
                app.insert(tk.CURRENT, text.get())
                app.mainloop()

            def getDataS(self):
                DataForDisplay = getData(self.Lb1.get(self.Lb1.curselection()), Base, engine, tags)
                text.set(DataForDisplay)
                app.delete('1.0', tk.END)
                app.insert(tk.CURRENT, text.get())
                app.mainloop()
                

            def viewDataS(self):
                DataForDisplay = view(self.Lb1.get(self.Lb1.curselection()), engine, tags)
                text.set(DataForDisplay)
                app.delete('1.0', tk.END)
                app.insert(tk.CURRENT, text.get())
                app.mainloop()
                
        
        root = tk.Tk()

        text = tk.StringVar()
        text.set('')


        app = App(master=root)
        app = tk.Text(root, height=30, width=100)
        app.pack(side="left",fill="both",expand=True)
        # scroll = tk.Scrollbar(app)
        # scroll.pack(side="right",fill="y",expand=False)
        app.insert(tk.END, text.get())
        app.mainloop()


                
if __name__ == '__main__':
    main()