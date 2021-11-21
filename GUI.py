import tkinter as tk
from tkinter import OptionMenu, ttk
from tkinter.constants import END

from CRC import Polynomial,CRCencoder

class CRC_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CRC")

        #MSG input variables  (binary,polynomial)
        self.msgTextLable = None
        self.msgPolyLable = None
        self.msgPoly = Polynomial('0')

        #gPoly input variables  (binary,polynomial)
        self.gPolyTextLable = None
        self.gPolyPolyLable = None
        self.gPoly = Polynomial('0')

        #gPoly option for combobox to chose Polys from
        self.gPolyOptions = [""]
        self.clicked = tk.StringVar()       
        self.dropGPoly = None

        #Type of specifying of creating of g Poly
        self.gPolyType = tk.StringVar()
        self.gPolyType.set("auto")

        #encoded output variables  (binary,polynomial)
        self.encodedMsgTextLable = None
        self.encodedMsgPolyLable = None
        self.encodedPoly=None

        #MSG input variables - decoding  (binary,polynomial)
        self.decodedMsgTextLable = None
        self.decodedMsgPolyLable = None

        #gPoly size Entries
        self.polyNEntry = None
        self.polyKEntry = None
        self.gPolySize = [0,0]

        self.coder = CRCencoder()

        tabControl = ttk.Notebook(self.root)

        self.encodeTab = ttk.Frame(tabControl)
        self.decodeTab = ttk.Frame(tabControl)

        tabControl.add(self.encodeTab, text='Encode')
        tabControl.add(self.decodeTab, text='Decode')
        tabControl.pack(expand=1, fill="both")

    def start(self):
        self.createEncodeTab()
        self.createDecodeTab()

        self.root.mainloop()

    def createEncodeTab(self): 
        #instrruction column 0
        ttk.Label(self.encodeTab, 
                text ="Binary:").grid(column = 0, 
                                    row = 1,
                                    padx = 10,
                                    pady = 10)
        ttk.Label(self.encodeTab, 
                text ="Polynomial:").grid(column = 0, 
                                    row = 2,
                                    padx = 10,
                                    pady = 10)
        ttk.Label(self.encodeTab, 
                text ="Enter Message:").grid(column = 0, 
                                    row = 3,
                                    padx = 10,
                                    pady = 10)
        ttk.Label(self.encodeTab, 
                text ="Generating poly:").grid(column = 0, 
                                    row = 4,
                                    padx = 10,
                                    pady = 10)
        ttk.Label(self.encodeTab, 
                text ="G. poly size (n,k):").grid(column = 0, 
                                    row = 5,
                                    padx = 10,
                                    pady = 10)
        
                            
        #Message info column 1
        ttk.Label(self.encodeTab, 
                text ="Message:").grid(column = 1, 
                                    row = 0,
                                    padx = 10,
                                    pady = 10)

            #Raw text
        self.msgTextLable=ttk.Label(self.encodeTab, 
                text ="")
        self.msgTextLable.grid(column = 1, 
                row = 1,
                padx = 10,
                pady = 10)
        
            #Poly representation
        self.msgPolyLable=ttk.Label(self.encodeTab, 
                text ="")
        self.msgPolyLable.grid(column = 1, 
                row = 2,
                padx = 10,
                pady = 10)


        #G Poly info column 2
        ttk.Label(self.encodeTab, 
                text ="Generating polynomial:").grid(column = 2, 
                                    row = 0,
                                    padx = 10,
                                    pady = 10) 
            #Raw text                         
        self.gPolyTextLable=ttk.Label(self.encodeTab, 
                text ="")
        self.gPolyTextLable.grid(column = 2, 
                row = 1,
                padx = 10,
                pady = 10)  

            #Poly representation
        self.gPolyPolyLable=ttk.Label(self.encodeTab, 
                text ="")
        self.gPolyPolyLable.grid(column = 2, 
                row = 2,
                padx = 10,
                pady = 10)      
        #msg entry box
        e1 =tk.Entry(self.encodeTab)
        e1.grid(column = 1,
                row =3)
        reg = self.root.register(self.messageInputValidation)
        e1.config(validate ="key",validatecommand =(reg, '%d','%S','%P'))

        #g poly entry
        self.createComBox(self.encodeTab,1,4)

        #g poly type (n,k) entry
        reg2 = self.root.register(self.gPolySizeValidation)

        f2 = tk.Frame(self.encodeTab)

        self.polyNEntry = tk.Entry(f2,name='polyN',width=5,state="readonly")        
        self.polyNEntry.config(validate="key",validatecommand =(reg2, '%d','%S','%P','%W'))
        self.polyNEntry.grid(column=0,row=0,padx = 2)

        self.polyKEntry = tk.Entry(f2,name='polyK',width=5,state="readonly")        
        self.polyKEntry.config(validate="key",validatecommand =(reg2, '%d','%S','%P','%W'))
        self.polyKEntry.grid(column=1,row=0,padx = 2)

        f2.grid(column = 1,
                row =5)


        #g poly type chckboxes
        f1 = tk.Frame(self.encodeTab)
        checkboxLabel = tk.Label(f1,text="G. poly options:",font=('Helvetica', 9, 'bold'))
        R1 = tk.Radiobutton(f1, text="automatic", value="auto", var=self.gPolyType,command = self.gPolyCheckBox)        
        R2 = tk.Radiobutton(f1, text="spicified by user", value="specify", var=self.gPolyType,command = self.gPolyCheckBox)
        R3 = tk.Radiobutton(f1, text="custom", value="custom", var=self.gPolyType,command = self.gPolyCheckBox)
        checkboxLabel.pack()
        R1.pack()
        R2.pack()
        R3.pack()

        f1.grid(column=2,row=4,rowspan=2)

        #encode btn
        btn = tk.Button(self.encodeTab,command=self.encode,text="Encode")
        btn.grid(column=1,row = 6)

    def createComBox(self,root,column,row):
        self.dropGPoly = ttk.Combobox(root,width = 15,textvariable = self.clicked,state="readonly")
        self.dropGPoly ['values'] = self.gPolyOptions
        self.dropGPoly.grid(column=column,row=row)

        self.dropGPoly.bind("<<ComboboxSelected>>",self.changeGPoly)
    
    def createInputBox(self,root,column,row):         
        self.dropGPoly =tk.Entry(root)
        self.dropGPoly.grid(column = column,
                row =row)
        reg = self.root.register(self.generatingInputValidation)
        self.dropGPoly.config(validate ="key",validatecommand =(reg, '%d','%S','%P'))
   
    def messageInputValidation(self,d,S,P):         
        if d == '0':
            #allow removal always
            self.changeMsg(P)            
            self.clicked.set("")            
            return True 
        if S == '1' or S =='0':
            #allow only input 1 or 0
            self.changeMsg(P)            
            self.clicked.set("")                     
            return True 
        elif len(S)>1:
            valid = True
            for char in S:
                if char == '1' or char =='0':
                    continue
                else:
                    valid = False
                    break  
            if valid:
                self.changeMsg(P)                
                self.clicked.set("")                         
                return True      
        return False

    def generatingInputValidation(self,d,S,P):
        if d == '0':
            #allow removal always
            self.changeGPolyFromEntry(P)            
            return True 
        if S == '1' or S =='0':
            #allow only input 1 or 0
            self.changeGPolyFromEntry(P)                            
            return True    
        return False

    def changeMsg(self,msg):
        self.msgTextLable.config(text=msg)
        if msg == "":
            self.msgPoly = None
            self.msgPolyLable.config(text = "")
            self.gPolyOptions = []
        else:
            #update msg info
            self.msgPoly = Polynomial(msg)
            
            
            self.msgPolyLable.config(text = self.msgPoly.getPolynomialRepresentation())
            #update gPoly options
            self.coder.setMessage(msg)
            self.coder.findgGeneratingPolyAutomatic()
            self.gPolyOptions = self.coder.gPolys
            if self.gPolyType.get()=="auto":                
                gPolyType=self.coder.findgGeneratingPolyAutomatic()

                self.polyNEntry.config(state="normal")
                self.polyKEntry.config(state="normal")

                self.polyNEntry.delete(0,END)
                self.polyNEntry.insert(0,gPolyType[0])

                self.polyKEntry.delete(0,END)
                self.polyKEntry.insert(0,gPolyType[1])

                self.polyNEntry.config(state="readonly")
                self.polyKEntry.config(state="readonly")

                self.dropGPoly['values'] = self.coder.gPolys
                self.gPolyOptions = self.coder.gPolys

            if self.gPolyType.get()=="specify":                                
                self.coder.findGeneratingPolys(int(self.gPolySize[0]),int(self.gPolySize[1]))                
                
                self.dropGPoly['values'] = self.coder.gPolys
                self.gPolyOptions = self.coder.gPolys


    def changeGPoly(self,event):
        self.gPolyTextLable.config(text=self.dropGPoly.get())
        self.gPoly=Polynomial(self.dropGPoly.get())
        self.coder.gPoly = self.gPoly
        self.gPolyPolyLable.config(text=self.coder.gPoly.getPolynomialRepresentation())
    
    def changeGPolyFromEntry(self,P):        
        self.gPolyTextLable.config(text=P)
        if P == '':
            self.gPoly = None
            self.gPolyPolyLable.config(text='')
        else:
            self.gPoly=Polynomial(P)           
            self.gPolyPolyLable.config(text=self.gPoly.getPolynomialRepresentation())

    def gPolyCheckBox(self):
        self.dropGPoly.destroy()        
        if self.gPolyType.get() == "auto":
            self.createComBox(self.encodeTab,1,4)
            self.polyNEntry.config(state="readonly")
            self.polyKEntry.config(state="readonly")
        elif self.gPolyType.get()=="specify":
            self.createComBox(self.encodeTab,1,4)            
            self.polyNEntry.config(state="normal")
            self.polyKEntry.config(state="normal")
        elif self.gPolyType.get()=="custom":
            self.createInputBox(self.encodeTab,1,4)
            self.polyNEntry.config(state="readonly")
            self.polyKEntry.config(state="readonly")
    
    def gPolySizeValidation(self,d,S,P,W):        
        if d == '0':
            #allow removal always
            self.changegPolySize(P,W)            
            return True 
        if len(P)>3:
            return False
        elif S.isdigit():            
            self.changegPolySize(P,W)                       
            return True 
        return False
    
    def changegPolySize(self,P,W):
        if P == "":
            P=0

        if W == '.!notebook.!frame.!frame.polyN': 
            
            self.gPolySize[0]=int(P)
        elif W == '.!notebook.!frame.!frame.polyK':   
            self.gPolySize[1]=int(P)

        if 0<self.gPolySize[0] and 0<self.gPolySize[1] and 0<=self.gPolySize[0]-self.gPolySize[1]<10:
            self.coder.findGeneratingPolys(int(self.gPolySize[0]),int(self.gPolySize[1]))                
                
            self.dropGPoly['values'] = self.coder.gPolys
            self.gPolyOptions = self.coder.gPolys 
        else:
            self.dropGPoly['values'] = []

    def encode(self):
        self.coder.setMessage(self.msgPoly.bin)
        self.coder.gPoly = self.gPoly
        msg =self.coder.encode()       
        
        self.updateEncodedMsg(msg)

    def updateEncodedMsg(self,msg):
        if self.encodedMsgTextLable is None:
            self.encodedMsgTextLable=ttk.Label(self.encodeTab)  
            self.encodedMsgTextLable.grid(column = 1, 
                                            row = 9,
                                            padx = 10,
                                            pady = 10)      
        self.encodedMsgTextLable.config(text =msg.getBinary())    
        #Poly representation
        if self.encodedMsgPolyLable is None:
            self.encodedMsgPolyLable=ttk.Label(self.encodeTab)
            self.encodedMsgPolyLable.grid(column = 1, 
                                            row = 10,
                                            padx = 10,
                                            pady = 10)
        self.encodedMsgPolyLable.config(text =msg.getPolynomialRepresentation())
        
        self.encodedPoly =msg

        #labels
        ttk.Label(self.encodeTab, 
                text ="Encoded message").grid(column = 0, 
                                    row = 9,
                                    padx = 10,
                                    pady = 10)
        ttk.Label(self.encodeTab, 
                text ="Polynomial representatnion").grid(column = 0, 
                                    row = 10,
                                    padx = 10,
                                    pady = 10)

        #change input on decode tab
        self.msgEntry.delete(0,END)
        self.msgEntry.insert(0,msg.getBinary())       

        self.gPolyEntry.delete(0,END)
        self.gPolyEntry.insert(0,self.gPoly.getBinary())
        
    def createDecodeTab(self):
        #instrruction column 0
        ttk.Label(self.decodeTab, 
                text ="Enter:").grid(column = 0, 
                                    row = 1,
                                    padx = 10,
                                    pady = 10)
        ttk.Label(self.decodeTab, 
                text ="Polynomial:").grid(column = 0, 
                                    row = 2,
                                    padx = 10,
                                    pady = 10)

        #Message column 1
        ttk.Label(self.decodeTab, 
                text ="Message:").grid(column = 1, 
                                    row = 0,
                                    padx = 10,
                                    pady = 10)

        self.msgEntry =tk.Entry(self.decodeTab,name='msg')
        self.msgEntry.grid(column = 1,
                row =1)
        reg = self.root.register(self.decodeMessageInputValidation)
        self.msgEntry.config(validate ="key",validatecommand =(reg, '%d','%S','%P','%W'))

        self.decodeMsgText = tk.Label(self.decodeTab,text="")
        self.decodeMsgText.grid(column=1,row=2)

        #Generating column 2
        ttk.Label(self.decodeTab, 
                text ="Generating polynomial").grid(column = 2, 
                                    row = 0,
                                    padx = 10,
                                    pady = 10)
        self.gPolyEntry =tk.Entry(self.decodeTab,name='gPoly')
        self.gPolyEntry.grid(column = 2,
                row =1)
        reg = self.root.register(self.decodeMessageInputValidation)
        self.gPolyEntry.config(validate ="key",validatecommand =(reg, '%d','%S','%P','%W'))

        self.decodedPolyText = tk.Label(self.decodeTab,text="")
        self.decodedPolyText.grid(column=2,row=2)

        #encode btn
        btn = tk.Button(self.decodeTab,command=self.decode,text="Decode")
        btn.grid(column=1,row = 3)

    def decodeMessageInputValidation(self,d,S,P,W):        
        if d == '0':
            #allow removal always
            self.changeDecodePoly(P,W)            
            return True 
        if S == '1' or S =='0':
            #allow only input 1 or 0 
            self.changeDecodePoly(P,W)                     
            return True 
        elif len(S)>1:
            valid = True
            for char in S:
                if char == '1' or char =='0':
                    continue
                else:
                    valid = False
                    break  
            if valid:
                self.changeDecodePoly(P,W)  
                return True 
        return False

    def changeDecodePoly(self,P,W):
        if W == '.!notebook.!frame2.msg':  
            if P =="":
                 self.decodeMsgText.config(text="")
                 return
            poly = Polynomial(P)         
            self.decodeMsgText.config(text=poly.getPolynomialRepresentation())
            self.encodedPoly = poly
        elif W=='.!notebook.!frame2.gPoly':
            if P =="":
                 self.decodedPolyText.config(text="")
                 return
            poly = Polynomial(P)   
            self.decodedPolyText.config(text=poly.getPolynomialRepresentation())
            self.gPoly = poly

    def decode(self):        
        self.coder.msg = self.encodedPoly
        self.coder.gPoly = self.gPoly        
        try:
            decodedMsg =self.coder.decode()
            print(decodedMsg)
            self.updateDecodedMsg(decodedMsg,self.coder.errorOn)
        except:
            pass

    def updateDecodedMsg(self,msg,errorPos):
        if self.decodedMsgTextLable is None:
            self.decodedMsgTextLable=ttk.Label(self.decodeTab)  
            self.decodedMsgTextLable.grid(column = 1, 
                                            row = 5,
                                            padx = 10,
                                            pady = 10)      
        self.decodedMsgTextLable.config(text =msg.getBinary())    
        #Poly representation
        if self.decodedMsgPolyLable is None:
            self.decodedMsgPolyLable=ttk.Label(self.decodeTab)
            self.decodedMsgPolyLable.grid(column = 1, 
                                            row = 6,
                                            padx = 10,
                                            pady = 10)
        self.decodedMsgPolyLable.config(text =msg.getPolynomialRepresentation())

        #description
        ttk.Label(self.decodeTab, 
                text ="Status:").grid(column = 0, 
                                    row = 4,
                                    padx = 10,
                                    pady = 10)   
        ttk.Label(self.decodeTab, 
                text ="Decoded Message:").grid(column = 0, 
                                    row = 5,
                                    padx = 10,
                                    pady = 10)
        ttk.Label(self.decodeTab, 
                text ="Polynomial:").grid(column = 0, 
                                    row = 6,
                                    padx = 10,
                                    pady = 10)
        #Status and found error position
        if errorPos is None:
            ttk.Label(self.decodeTab, 
                text ="Trasmition without error").grid(column = 1, 
                                    row = 4,
                                    padx = 10,
                                    pady = 10) 
        else:
            ttk.Label(self.decodeTab, 
                text =f"Error found on position {errorPos}").grid(column = 1, 
                                    row = 4,
                                    padx = 10,
                                    pady = 10) 

    def instertWithSuperscription(self,string,label):
        label.tag_configure("s", offset=5)
        s = False
        for c in string:
            if c == "^":
                s = True
                continue
            if s == True:
                label.insert("insert",c,"s")
                s = False
                continue
            label.insert("insert",c)
gui = CRC_GUI()
gui.start()

