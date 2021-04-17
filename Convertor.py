import json
import datetime
import urllib.request
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import Tk, StringVar, ttk

root = Tk()
root.title('ALL IN ONE CONVERTER')
root.geometry("450x550")

# background for main display
bg = PhotoImage(file="icons/bg.png")
# Show image using label
label1 = Label(root, image=bg)
label1.place(x=0, y=0)
labelfont = ('ariel', 56, 'bold')
titlelabel = Label(root, text='ALL IN ONE CONVERTER', font=("Trajan Pro", 16), justify=CENTER)
titlelabel.place(relx=0.5, rely=0.05, anchor=CENTER)


##########################################  Currency Convertor   ##############################################

def currencyconverter():
    api = "bd2cc1412d9713443843bd85"
    ids = {"US Dollar": 'USD', "Euros": 'EUR', "Indian Rupees": 'INR', "South African Rand": 'ZAR',
           "Arab Emirates Dirham": 'AED', "Pound Sterling": 'GBP', "Japanese Yen": 'JPY', "Yuan Renminbi": 'CNY'}
    values = []
    date = []

    def hist(data, frm, to):
        html = urllib.request.urlopen("https://v6.exchangerate-api.com/v6/%s/history/%s/%s/%s/%s"
                                      % (api, frm, data[0], data[1], data[2]))
        ans = html.read().decode('utf-8')
        res = json.loads(ans)
        print(res)
        if to in res["conversion_rates"]:
            print(res["conversion_rates"][to])
            values.append(res["conversion_rates"][to])
            return 1
        else:
            print('data is not available')
            return 0


    def convert(amt, frm, to):
        html = urllib.request.urlopen("https://v6.exchangerate-api.com/v6/%s/pair/%s/%s/%f" % (api, frm, to, amt))
        ans = html.read().decode('utf-8')
        res = json.loads(ans)

        return res['conversion_result'], res['conversion_rate']

    def callback():
        try:
            amt = float(in_field.get())

        except ValueError:
            out_amt.set('Invalid input')
            return None
        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None
        else:
            global frm
            frm = ids[in_unit.get()]
            global to
            to = ids[out_unit.get()]

            t1, t2 = convert(amt, frm, to)
            out_amt.set(t1)
            st = "conversion rate  " + frm + " to " + to + " = " + str(t2)
            tl1 = Label(mainframe, text=st, font=("Arial", 12, "bold"), justify=CENTER).grid(column=2, row=4)


    root = Toplevel()
    root.title("Currency Converter")

    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='green')

    # Create style for the first frame
    s.configure('Frame1.TFrame', background='alice blue')
    # initiate frame
    mainframe = ttk.Frame(root, padding="3 3 12 12", style='Frame1.TFrame')
    mainframe.pack(fill=BOTH, expand=1)

    titleLabel = Label(mainframe, text="Currency Converter", font=("Arial", 12, "bold"),
                       justify=CENTER).grid(column=1, row=1)
    in_amt = StringVar()
    in_amt.set('0')
    out_amt = StringVar()

    in_unit = StringVar()
    out_unit = StringVar()
    in_unit.set('Select Unit')
    out_unit.set('Select Unit')

    # Add input field
    in_field = ttk.Entry(mainframe, width=20, textvariable=in_amt)
    in_field.grid(row=1, column=2, sticky=(W, E))

    # Add drop-down for input unit
    in_select = OptionMenu(mainframe, in_unit, "US Dollar", "Euros", "Indian Rupees", "South African Rand",
                           "Arab Emirates Dirham", "Pound Sterling", "Japanese Yen",
                           "Yuan Renminbi").grid(column=3, row=1, sticky=W)

    # Add output field and drop-down
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=2, row=3, sticky=(W, E))
    in_select = OptionMenu(mainframe, out_unit, "US Dollar", "Euros", "Indian Rupees", "South African Rand",
                           "Arab Emirates Dirham", "Pound Sterling", "Japanese Yen",
                           "Yuan Renminbi").grid(column=3, row=3, sticky=W)

    calc_button = ttk.Button(mainframe, text="Calculate", command=callback).grid(column=2, row=2, sticky=E)


    def chart():
        x = str(datetime.datetime.now())
        words = x.split('-')
        c_year = words[0]
        c_month = words[1]
        temp = words[2].split(' ')
        c_date = temp[0]
        f = 1

        for i in range(10):
            t = 270
            a_date = datetime.date(int(c_year), int(c_month), int(c_date))
            days = datetime.timedelta(int(t - i * (30)))
            new_date = str(a_date - days)
            date.append(new_date)
            data = new_date.split('-')
            print( "frm :" + str(frm) + " to :" + str(to))
            f = hist(data, frm, to)
            if f==0:
                l1 = Label(mainframe, text="data is not available", font=("Arial", 12, "bold"),
                           justify=CENTER).grid(column=2, row=10)
                l1.distroy()
                break


        if f == 1:
            fig = plt.figure()
            plt.style.use('seaborn')
            print(values)
            plt.plot_date(date, values, linestyle='solid')
            plt.title('conversion chart')
            plt.xlabel('date')
            plt.ylabel('value')
            plt.xticks(rotation=90)
            # plt.show()
            values.clear()
            print("values")
            print(values)
            date.clear()
            print("date")
            print(date)
            plt.tight_layout()
            tl2 = Label(mainframe, text=plt.show(), font=("Arial", 12, "bold"),
                        justify=CENTER).grid(column=2, row=7)


    plt_button = ttk.Button(mainframe, text="Historical values", command=chart).grid(column=2, row=6, sticky=E)
    tl2 = Label(mainframe, text="Historical values will take some time", font=("Arial", 12, "bold"),
                justify=CENTER).grid(column=2, row=7)


    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    in_field.focus()

############################################   Temperature Convertor   #######################################

def temperatureconvertor():
    factors = {'nmi': 1852, 'mi': 1609.34, 'yd': 0.9144, 'ft': 0.3048, 'inch': 0.0254, 'km': 1000, 'm': 1, 'cm': 0.01,
               'mm': 0.001}
    ids = {'celsius(C)': 'c', 'fahrenheit(F)': 'f'}

    def convert(amt, frm, to):
        if frm == 'c' and to == 'f':
            ans = (amt * 9 / 5 + 32)
            return ans
        elif frm == 'f' and to == 'c':
            ans = ((amt - 32) * (5 / 9))
            return ans
        elif frm == to:
            return amt

    def reset():
        in_unit.set(int(0))
        out_unit.set(int(0))

    def callback():
        try:
            amt = float(in_field.get())
        except ValueError:
            out_amt.set('Invalid input')
            return None
        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None
        else:
            frm = ids[in_unit.get()]
            to = ids[out_unit.get()]
            out_amt.set(convert(amt, frm, to))

    # initiate window
    root = Toplevel()
    root.title("Temperature Converter")

    # initiate frame
    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='green')

    # Create style for the first frame
    s.configure('Frame1.TFrame', background='alice blue')
    mainframe = ttk.Frame(root, padding="3 3 12 12", style='Frame1.TFrame')
    mainframe.pack(fill=BOTH, expand=1)
    titleLabel = Label(mainframe, text="Temperature Converter", font=("Arial", 12, "bold"),
                       justify=CENTER).grid(column=1,row=1)

    in_amt = StringVar()
    in_amt.set('0')
    out_amt = StringVar()

    in_unit = StringVar()
    out_unit = StringVar()
    in_unit.set('Select Unit')
    out_unit.set('Select Unit')

    # Add input field
    in_field = ttk.Entry(mainframe, width=20, textvariable=in_amt)
    in_field.grid(row=1, column=2, sticky=(W, E))

    # Add drop-down for input unit
    in_select = OptionMenu(mainframe, in_unit, "celsius(C)", "fahrenheit(F)").grid(column=3, row=1, sticky=W)

    # Add output field and drop-down
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=2, row=3, sticky=(W, E))
    in_select = OptionMenu(mainframe, out_unit, "celsius(C)", "fahrenheit(F)").grid(column=3, row=3, sticky=W)

    calc_button = ttk.Button(mainframe, text="Calculate", command=callback).grid(column=2, row=2, sticky=E)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    in_field.focus()


#########################################   Length Convertor   ########################################

def lengthconverter():
    # factors to multiply to a value to convert from the following units to meters(m)
    factors = {'nmi': 1852, 'mi': 1609.34, 'yd': 0.9144, 'ft': 0.3048, 'inch': 0.0254, 'km': 1000, 'm': 1, 'cm': 0.01,
               'mm': 0.001}
    ids = {"Nautical Miles": 'nmi', "Miles": 'mi', "Yards": 'yd', "Feet": 'ft', "Inches": 'inch', "Kilometers": 'km',
           "meters": 'm', "centimeters": 'cm', "millileters": 'mm'}

    # function to convert from a given unit to another
    def convert(amt, frm, to):
        if frm != 'm':
            amt = amt * factors[frm]
            return amt / factors[to]
        else:
            return amt / factors[to]

    def callback():
        try:
            amt = float(in_field.get())
        except ValueError:
            out_amt.set('Invalid input')
            return None
        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None
        else:
            frm = ids[in_unit.get()]
            to = ids[out_unit.get()]
            out_amt.set(convert(amt, frm, to))

    # initiate window
    root = Toplevel()
    root.title("Length Converter")

    # initiate frame
    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='green')

    # Create style for the first frame
    s.configure('Frame1.TFrame', background='alice blue')
    mainframe = ttk.Frame(root, padding="3 3 12 12", style='Frame1.TFrame')
    mainframe.pack(fill=BOTH, expand=1)
    titleLabel = Label(mainframe, text="Length Converter", font=("Arial", 12, "bold"),
                       justify=CENTER).grid(column=1,row=1)

    in_amt = StringVar()
    in_amt.set('0')
    out_amt = StringVar()

    in_unit = StringVar()
    out_unit = StringVar()
    in_unit.set('Select Unit')
    out_unit.set('Select Unit')

    # Add input field
    in_field = ttk.Entry(mainframe, width=20, textvariable=in_amt)
    in_field.grid(row=1, column=2, sticky=(W, E))

    # Add drop-down for input unit
    in_select = OptionMenu(mainframe, in_unit, "Nautical Miles", "Miles", "Yards", "Feet", "Inches", "Kilometers",
                           "meters", "centimeters", "millileters").grid(column=3, row=1, sticky=W)

    # Add output field and drop-down
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=2, row=3, sticky=(W, E))
    in_select = OptionMenu(mainframe, out_unit, "Nautical Miles", "Miles", "Yards", "Feet", "Inches", "Kilometers",
                           "meters", "centimeters", "millileters").grid(column=3, row=3, sticky=W)

    calc_button = ttk.Button(mainframe, text="Calculate", command=callback).grid(column=2, row=2, sticky=E)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    in_field.focus()



#########################################   Weight Convertor   ################################################

def weightconverter():
    # factors to multiply to a value to convert from the following units to meters(m)
    factors = {'kg': 1000, 'hg': 100, 'dg': 10, 'g': 1, 'deg': 0.1, 'cg': 0.01, 'mg': 0.001}
    ids = {"Kilogram": 'kg', "Hectagram": 'hg', "Decagram": 'dg', "Decigram": 'deg', "gram": 'g',
           "Centigram": 'cg', "Milligram": 'mg'}

    # function to convert from a given unit to another
    def convert(amt, frm, to):
        if frm != 'g':
            amt = amt * factors[frm]
            return amt / factors[to]
        else:
            return amt / factors[to]

    def callback():
        try:
            amt = float(in_field.get())
        except ValueError:
            out_amt.set('Invalid input')
            return None
        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None
        else:
            frm = ids[in_unit.get()]
            to = ids[out_unit.get()]
            out_amt.set(convert(amt, frm, to))

    # initiate window
    root = Toplevel()
    root.title("Weight Converter")
    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='green')

    # Create style for the first frame
    s.configure('Frame1.TFrame', background='alice blue')
    # initiate frame
    mainframe = ttk.Frame(root, padding="3 3 12 12", style='Frame1.TFrame')
    mainframe.pack(fill=BOTH, expand=1)
    titleLabel = Label(mainframe, text="Weight Converter", font=("Arial", 12, "bold"),
                       justify=CENTER).grid(column=1,row=1)

    in_amt = StringVar()
    in_amt.set('0')
    out_amt = StringVar()

    in_unit = StringVar()
    out_unit = StringVar()
    in_unit.set('Select Unit')
    out_unit.set('Select Unit')

    # Add input field
    in_field = ttk.Entry(mainframe, width=20, textvariable=in_amt)
    in_field.grid(row=1, column=2, sticky=(W, E))

    # Add drop-down for input unit
    in_select = OptionMenu(mainframe, in_unit, "Kilogram", "Hectagram", "Decagram", "gram", "Decigram",
                           "Centigram","Milligram").grid(column=3, row=1, sticky=W)

    # Add output field and drop-down
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=2, row=3, sticky=(W, E))
    in_select = OptionMenu(mainframe, out_unit, "Kilogram", "Hectagram", "Decagram", "gram", "Decigram",
                           "Centigram","Milligram").grid(column=3, row=3, sticky=W)

    calc_button = ttk.Button(mainframe, text="Calculate", command=callback).grid(column=2, row=2, sticky=E)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    in_field.focus()


#########################################   Area Convertor   #########################################

def areaconvertor():
    # factors to multiply to a value to convert from the following units to meters(m)
    ids = {"square meter": 'smeter', "square km": 'skmeter', "square rood": 'srood', "square cm": 'scmeter',
                   "square foot": 'sfoot',"square inch": 'sinch', "square mile": 'smile', "milimeter": 'mmeter',
                   "square rod": 'srod',"square yard": 'syard', "square township": 'stownship', "square acre": 'sacre',
                   "square are": 'sare',"square barn": 'sbarn', "square hectare": 'shectare',
                    "square homestead": 'shomestead'}

    factors = {'smeter': 1, 'skmeter': 1000000, 'srood': 1011.7141056, 'scmeter': 0.0001,
                   'sfoot': 0.09290304,'sinch': 0.00064516, 'smile': 2589988.110336, 'mmeter': 0.000001,
                   'srod': 25.29285264,'syard': 0.83612736, 'stownship': 93239571.9721, 'sacre': 4046.8564224,
                   'sare': 100,'sbarn': 1e-28, 'shectare': 10000, 'shomestead': 647497.027584}

    # function to convert from a given unit to another
    def convert(amt, frm, to):
        if frm != 'g':
            amt = amt * factors[frm]
            return amt / factors[to]
        else:
            return amt / factors[to]

    def callback():
        try:
            amt = float(in_field.get())
        except ValueError:
            out_amt.set('Invalid input')
            return None
        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None
        else:
            frm = ids[in_unit.get()]
            to = ids[out_unit.get()]
            out_amt.set(convert(amt, frm, to))

    # initiate window
    root = Toplevel()
    root.title("Area Converter")
    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='green')

    # Create style for the first frame
    s.configure('Frame1.TFrame', background='alice blue')
    # initiate frame
    mainframe = ttk.Frame(root, padding="3 3 12 12", style='Frame1.TFrame')
    mainframe.pack(fill=BOTH, expand=1)
    titleLabel = Label(mainframe, text="Area Converter", font=("Arial", 12, "bold"),
                       justify=CENTER).grid(column=1,row=1)

    in_amt = StringVar()
    in_amt.set('0')
    out_amt = StringVar()

    in_unit = StringVar()
    out_unit = StringVar()
    in_unit.set('Select Unit')
    out_unit.set('Select Unit')

    # Add input field
    in_field = ttk.Entry(mainframe, width=20, textvariable=in_amt)
    in_field.grid(row=1, column=2, sticky=(W, E))

    # Add drop-down for input unit
    in_select = OptionMenu(mainframe, in_unit, "square meter", "square km", "square rood", "square cm", "square foot",
                   "square inch", "square mile", "milimeter", "square rod", "square yard", "square township",
                    "square acre", "square are", "square barn", "square hectare",
                    "square homestead").grid(column=3, row=1, sticky=W)

    # Add output field and drop-down
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=2, row=3, sticky=(W, E))
    in_select = OptionMenu(mainframe, out_unit, "square meter", "square km", "square rood", "square cm", "square foot",
                   "square inch", "square mile", "milimeter", "square rod", "square yard", "square township",
                    "square acre", "square are", "square barn", "square hectare",
                    "square homestead").grid(column=3, row=3, sticky=W)

    calc_button = ttk.Button(mainframe, text="Calculate", command=callback).grid(column=2, row=2, sticky=E)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    in_field.focus()



###################################################################################################################
################################   Currency Convertor button   ##################################################

# Creating a photoimage object to use image
photo1 = PhotoImage(file=r"icons/currency.png")
# Resizing image to fit on button
photoimage1 = photo1.subsample(13, 13)

widget1 = Button(root, text="    Currency converter", bg="black", fg="white", font=("Arial", 14, "bold"),
                relief=RAISED, bd=5,justify=CENTER, overrelief=GROOVE, command=currencyconverter,
                image=photoimage1, compound = LEFT, width=300, border=0).place(relx=0.5, rely=0.2, anchor=CENTER)

###################################   Temperature Convertor button   ############################################

# Creating a photoimage object to use image
photo2 = PhotoImage(file=r"icons/temperature.png")
# Resizing image to fit on button
photoimage2 = photo2.subsample(13, 13)

widget2 = Button(root, text="    Temperature converter", bg="black", fg="white", font=("Arial", 14, "bold"),
                relief=RAISED, bd=5,justify=CENTER, overrelief=GROOVE, command=temperatureconvertor,
                image=photoimage2, compound = LEFT, width=300, border=0).place(relx=0.5, rely=0.35, anchor=CENTER)

###################################   Length Convertor button   ###############################################

# Creating a photoimage object to use image
photo3 = PhotoImage(file=r"icons/length.png")
# Resizing image to fit on button
photoimage3 = photo3.subsample(13, 13)

widget3 = Button(root, text="    Length converter", bg="black", fg="white", font=("Arial", 14, "bold"),
                relief=RAISED, bd=5,justify=CENTER, overrelief=GROOVE, command=lengthconverter,
                image=photoimage3, compound = LEFT, width=300, border=0).place(relx=0.5, rely=0.5, anchor=CENTER)

####################################   Weight Convertor button   ##############################################

# Creating a photoimage object to use image
photo4 = PhotoImage(file=r"icons/weight.png")
# Resizing image to fit on button
photoimage4 = photo4.subsample(13, 13)

widget4 = Button(root, text="    Weight converter", bg="black", fg="white", font=("Arial", 14, "bold"),
                relief=RAISED, bd=5,justify=CENTER, overrelief=GROOVE, command=weightconverter,
                image=photoimage4, compound = LEFT, width=300, border=0).place(relx=0.5, rely=0.65, anchor=CENTER)

####################################   Area Convertor button   ###############################################

# Creating a photoimage object to use image
photo5 = PhotoImage(file=r"icons/area.png")
# Resizing image to fit on button
photoimage5 = photo5.subsample(13, 13)

widget5 = Button(root, text="    Area converter", bg="black", fg="white", font=("Arial", 14, "bold"),
                relief=RAISED, bd=5,justify=CENTER, overrelief=GROOVE, command=areaconvertor,
                image=photoimage5, compound = LEFT, width=300, border=0).place(relx=0.5, rely=0.8, anchor=CENTER)

########################################   Quit button   ####################################################

# Creating a photoimage object to use image
photo6 = PhotoImage(file=r"icons/quit.png")
# Resizing image to fit on button
photoimage6 = photo6.subsample(13, 13)

widget6 = Button(None, text="    QUIT", bg="black", fg="white", font=("Arial", 14, "bold"),
                relief=RAISED, bd=5,justify=CENTER, overrelief=GROOVE, command=root.destroy,
                image=photoimage6, compound = LEFT, width=150, border=0).place(relx=0.5, rely=0.93, anchor=CENTER)

######################################################################################################################

root.mainloop()