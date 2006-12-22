import sys
from Tkinter import *
import tkMessageBox

#options:
#num_of_frets=30
#scale_length=27
#print_in_fractions=1

#scale_length=float(scale_length)

class App(Frame):
###################################################################################################
# main form
###################################################################################################
    def __init__(self, master=None):
        Frame.__init__(self, master, relief='sunken', border=1)
        self.pack(fill=BOTH,expand=1,side=TOP)
        self.topframe=Frame(self)
        self.topframe.grid(row=0,column=0,sticky=E+W)
        #
        self.numfretlabel=Label(self.topframe,text="Number of frets:")
        self.numfretlabel.grid(row=0,column=0,sticky=E)
        self.numfretvalue=StringVar()
        self.numfretvalue.set("24")
        self.numfretentry=Entry(self.topframe,textvariable=self.numfretvalue,width=5)
        self.numfretentry.grid(row=0,column=1,sticky=SW,pady=4)
        self.numfretscale=Scale(self.topframe,
                                variable=self.numfretvalue, from_=1, to=34,
                                orient=HORIZONTAL,showvalue=FALSE)
        self.numfretscale.grid(row=0,column=2,sticky=SW)
        #
        self.scalelengthlabel=Label(self.topframe,text="Scale Length:")
        self.scalelengthlabel.grid(row=1,column=0,sticky=E)
        self.scalelengthvalue=StringVar()
        self.scalelengthvalue.set("26.0")
        self.scalelengthentry=Entry(self.topframe,textvariable=self.scalelengthvalue,width=5)
        self.scalelengthentry.grid(row=1,column=1,sticky=W)
        #self.scalelengthscale=Scale(self.topframe,
        #                        variable=self.scalelengthvalue, from_=12.00, to=36.00,
        #                        orient=HORIZONTAL,showvalue=FALSE,resolution=0.25)
        #self.scalelengthscale.grid(row=1,column=2,sticky=SW)
        #
        self.decfracframe=Frame(self)
        self.decfracframe.grid(row=1,column=0,sticky=E+W)
        self.decimal_or_fraction = StringVar()
        self.decimal_or_fraction.set("fraction")
        self.decimal_radiobutton = Radiobutton(self.decfracframe,
                                               variable=self.decimal_or_fraction,
                                               value="decimal",
                                               text="Decimal")
        self.decimal_radiobutton.grid(row=0,column=0,padx=3,pady=3)
        self.fraction_radiobutton = Radiobutton(self.decfracframe,
                                               variable=self.decimal_or_fraction,
                                               value="fraction",
                                               text="Fraction")
        self.fraction_radiobutton.grid(row=0,column=1,padx=3,pady=3)
        #self.fractionsizeframe=Frame(self)
        #self.fractionsizeframe.grid(row=2,column=0,sticky=E+W)
        self.fraction_size = StringVar()
        self.fraction_size.set("32")
        self.fraction_size_menu=OptionMenu(self.decfracframe,
                                           self.fraction_size, "8","16","32","64")
        self.fraction_size_menu.grid(row=0,column=2,padx=3,pady=3)
        #
        self.calculatebutton=Button(self,text="Calculate",command=self.calculate)
        self.calculatebutton.grid(row=3,column=0,sticky=E+W)
        #
        self.text_area=Text(self,width=41,height=28,font=("Courier",10))
        self.text_area.grid(row=4,column=0,sticky=E+W)
        #
    def copytext(self):
        alltext=self.text_area.get("1.0",END)
        self.clipboard_clear()
        self.clipboard_append(alltext)
    def calculate(self):
        self.text_area.delete("1.0",END)
        results=CalcFretLocation(self.scalelengthvalue.get(),self.numfretvalue.get())
        self.SendResultsToTextBox(results,
                                  self.scalelengthvalue.get(),
                                  self.numfretvalue.get(),
                                  self.decimal_or_fraction.get())
    def SendResultsToTextBox(self, results,scale_length,num_of_frets,print_in_fractions):
        #self.text_area.delete(0,END) 
        num_of_frets=int(float(num_of_frets))
        self.text_area.insert(END, "Scale Length:"+str(scale_length)+"\n")
        self.text_area.insert(END, "\n")
        self.text_area.insert(END,  "Fret  Distance       Remainder  Distance\n")
        self.text_area.insert(END,  "      From Previous             From Nut\n")
        for fret in range(1,num_of_frets+1):
            if print_in_fractions == "decimal":
                #print "degub 1"
                self.text_area.insert(END,  "%-6d%-15.3f%-11.3f%-8.3f\n" % (fret,
                                                results[fret]["dist_from_previous"],
                                                results[fret]["string_remainder"],
                                                results[fret]["total_dist_from_nut"]))
            else:
                #print "degub 2"
                self.text_area.insert(END,  "%-6d%-15s%-11s%-8s\n" % (fret,
                                          Dec2Frac(results[fret]["dist_from_previous"],self.fraction_size.get()),
                                          Dec2Frac(results[fret]["string_remainder"],self.fraction_size.get()),
                                          Dec2Frac(results[fret]["total_dist_from_nut"],self.fraction_size.get())))
    def about(self):
        tkMessageBox.showinfo("About","FretCalc\nBy Blake Garretson\n\xA9 2001")

def Dec2Frac(x, largest_denominator=32):
    largest_denominator=int(largest_denominator)
    if not x >= 0:
        raise ValueError("x must be >= 0")
    scaled = int(round(x * largest_denominator))
    whole, leftover = divmod(scaled, largest_denominator)
    if leftover:
        while leftover % 2 == 0:
            leftover >>= 1
            largest_denominator >>= 1
    if leftover==0:
        final_string=str(whole)
    elif whole==0:
        final_string=str(leftover)+"/"+str(largest_denominator)
    else:
        final_string=str(whole)+" "+str(leftover)+"/"+str(largest_denominator)
    return final_string

def CalcFretLocation(scale_length=26,num_of_frets=12):
    num_of_frets=int(float(num_of_frets))
    scale_length=float(scale_length)
    MagicNumber=17.817
    fret_list=range(1,int(num_of_frets)+1)
    results={}
    total_dist_from_nut=0.0
    dist_from_previous=0.0
    string_remainder=scale_length
    for fret in fret_list:
        dist_from_previous=string_remainder/MagicNumber
        total_dist_from_nut=total_dist_from_nut+dist_from_previous
        string_remainder=string_remainder-dist_from_previous
        results[fret]={"dist_from_previous":dist_from_previous,
                       "string_remainder":string_remainder,
                       "total_dist_from_nut":total_dist_from_nut}
    return results

root = Tk()
root.title("FretCalc")
AppInstance=App(root)
menubar = Menu(root)
# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Calculate", command=AppInstance.calculate)
filemenu.add_command(label="Copy All", command=AppInstance.copytext)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
#
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=AppInstance.about)
menubar.add_cascade(label="Help", menu=helpmenu)
#
root.config(menu=menubar)
root.mainloop()
