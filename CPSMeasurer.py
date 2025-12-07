import tkinter, tkinter.ttk, tkinter.font, tkinter.messagebox, os.path, random, tkinter.font

root = tkinter.Tk()
style = tkinter.ttk.Style(root)
root.tk.call('source', f'{os.path.dirname(__file__)}\\Azure-ttk-theme-main\\Azure-ttk-theme-main\\azure.tcl')
style.theme_use('azure-dark')
root.tk.call("set_theme", "dark")


root.title("Clicks Per Second")
#performing a dilation (thank you to my geometry teacher for teaching me this):
k = .5
root.geometry(f"{int(root.winfo_screenwidth()*k)}x{int(root.winfo_screenheight()*k)}")
root.minsize(width=int(root.winfo_screenwidth()*k), height=int(root.winfo_screenheight()*k))
root.update_idletasks()
#center the window:
K = 2
root.geometry(f"{int(root.winfo_screenwidth()*k)}x{int(root.winfo_screenheight()*k)}+{int(int(root.winfo_screenwidth())//K - int(root.winfo_screenwidth()*k // K))}+{int(int(root.winfo_screenheight()*k // K))}")

FontList = {"Tahoma", "Calibri", "Verdana", "Microsoft New Tai Lue", "Arial CYR", "Arial", "Yu Gothic UI Semilight", "Courier New Baltic", "Microsoft Himalaya", "Georgia", "Ink Free", "Sylfaen", "Courier New", "Bahnschrift SemiCondensed"}
Font = tkinter.font.Font(family=random.choice(list(FontList)), size=20)
print(Font.actual()["family"])

MainFrame = tkinter.ttk.Frame(root)
MainFrame.pack(expand=True)

CPSFrame = tkinter.ttk.Frame(MainFrame)
CPSFrame.pack(expand=True)
CPSLabel = tkinter.ttk.Label(CPSFrame, text="0 clicks per second", font=Font)
CPSLabel.pack(padx=10, expand=True)
MaxCPSLabel = tkinter.ttk.Label(CPSFrame, text="Max CPS: 0", font=Font)
MaxCPSLabel.pack(padx=10, expand=True)
LastCPSLabel = tkinter.ttk.Label(CPSFrame, text="Last CPS: 0", font=Font)
LastCPSLabel.pack(padx=10, expand=True)
#HighestLabel = tkinter.ttk.Label(CPSFrame, text="CPS: 0, 0, 0", font=Font) #for debugging
#HighestLabel.pack(padx=10, expand=True)
def Quit():
    root.destroy()
    exit()

root.protocol("WM_DELETE_WINDOW", Quit)
QuitButton = tkinter.ttk.Button(MainFrame, text="Click to Exit", command=Quit)
QuitButton.pack(pady=10, expand=True, side="bottom")

Max = [0, 0]

#reset cps to zero every second
def reset_counter():
    global cps, Max
    Max[Max.index(min(Max))] = cps
    MaxCPSLabel['text'] = f"Max CPS: {max(Max)}"
    LastCPSLabel['text'] = f"Last CPS: {cps}"
    #HighestLabel['text'] = f"CPS: {', '.join(map(str, Max))}"
    CPSLabel['text'] = f'{(cps := 0)} clicks per second'
    root.after(1000, reset_counter)

#increment cps and publish results
def click_counter(event):
    global cps
    cps += 1
    CPSLabel['text'] = f'{cps} clicks per second'
    
root.bind_all('<1>', click_counter) #left click
root.bind_all('<3>', click_counter) #right click

cps = 0
reset_counter()

root.mainloop()   

tkinter.mainloop()