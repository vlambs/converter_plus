import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

# ~~ Consts ~~
CURRENCY_UNITS_LIST=['USD', 'EUR','GBP']
EXCHANGE_RATES = {
    'EUR to USD': 1.10,
    'EUR to GBP': 0.86,
    'USD to EUR': 0.91,
    'USD to GBP': 0.79,
    'GBP to EUR': 1.16,
    'GBP to USD': 1.27
}
TEMPERATURE_UNITS_LIST=['Celsius', 'Fahrenheit', 'Kelvin']
TEMPERATURE_CONVERSION_FUNCTIONS = {
    ('Celsius', 'Fahrenheit'): lambda celsius: celsius * 9/5 + 32,
    ('Fahrenheit', 'Celsius'): lambda fahrenheit: (fahrenheit - 32) * 5/9,
    ('Celsius', 'Kelvin'): lambda celsius: celsius + 273.15,
    ('Kelvin', 'Celsius'): lambda kelvin: kelvin - 273.15,
    ('Fahrenheit', 'Kelvin'): lambda fahrenheit: (fahrenheit - 32) * 5/9 + 273.15,
    ('Kelvin', 'Fahrenheit'): lambda kelvin: kelvin * 9/5 - 459.67
}

DISTANCE_UNITS_LIST=['KM', 'MILES']
DISTANCE_CONVERSION = {
    'KM to MILES': 0.621371,
    'MILES to KM': 1.60934
}

# ~~ Events ~~ 
def toogle_theme():
    if button_theme['text'] == 'Dark':
        window.style.theme_use(themename='darkly')
        button_theme['text'] = 'Light'
    else:
        window.style.theme_use(themename='journal')
        button_theme['text'] = 'Dark'

def swap_currencies():
    temp = combobox_currency_from.current()
    combobox_currency_from.current(combobox_currency_to.current())
    combobox_currency_to.current(temp)

def swap_temperatures():
    temp = combobox_temperature_from.current()
    combobox_temperature_from.current(combobox_temperature_to.current())
    combobox_temperature_to.current(temp)

def swap_distances():
    temp = combobox_distance_from.current()
    combobox_distance_from.current(combobox_distance_to.current())
    combobox_distance_to.current(temp)


def convert_currency():
    if len(input_currency_value.get()) > 0: 
        from_currency = combobox_currency_from_value.get()
        to_currency = combobox_currency_to_value.get()
        amount = float(input_currency_value.get())
        converted_value = converted_currency_value.get()

        conversion_pair = f'{from_currency} to {to_currency}'
        exchange_rate = EXCHANGE_RATES.get(conversion_pair)
        if exchange_rate is not None:
            converted_amount = amount * exchange_rate
            converted_value = f'{converted_amount:.2f} {to_currency}'
        else:
            converted_value = 'Conversion not supported'
    else:
        converted_value = 'No input amount'
    converted_currency_value.set(converted_value)

def convert_temperature():
    # Récupérer les valeurs des ComboBox et la température à convertir
    from_temperature = combobox_temperature_from_value.get()
    to_temperature = combobox_temperature_to_value.get()
    temperature = float(input_temperature_value.get())

    # Identifier la paire de conversion et récupérer la fonction de conversion
    conversion_pair = (from_temperature, to_temperature)
    conversion_function = TEMPERATURE_CONVERSION_FUNCTIONS.get(conversion_pair)
    converted_value = converted_temperature_value.get()

    if conversion_function is not None:
        # Effectuer la conversion en appelant la fonction de conversion
        converted_temperature = conversion_function(temperature)
        converted_value = f'{converted_temperature:.2f} {to_temperature}'
    else:
        converted_value = 'Conversion non prise en charge'
    converted_temperature_value.set(converted_value)


def convert_distance():
    if len(input_distance_value.get()) > 0: 
        from_distance = combobox_distance_from_value.get()
        to_distance = combobox_distance_to_value.get()
        amount = float(input_distance_value.get())
        converted_value = converted_distance_value.get()

        conversion_pair = f'{from_distance} to {to_distance}'
        exchange_rate = DISTANCE_CONVERSION.get(conversion_pair)
        if exchange_rate is not None:
            converted_amount = amount * exchange_rate
            converted_value = f'{converted_amount:.2f} {to_distance}'
        else:
            converted_value = 'Conversion not supported'
    else:
        converted_value = 'No input amount'
    converted_distance_value.set(converted_value)

# ~~ UI ~~
window = ttk.Window(themename = 'journal')
window.title('ConverterPlus')
window.geometry('500x400')

# header
header = tk.Frame(window)
ttk.Label(header, text='Converter Plus', font='Calibri 24').pack(side=tk.RIGHT)
button_theme = tk.Button(
    header, 
    text='Dark', 
    command=toogle_theme
)
button_theme.pack()
header.pack(expand=True)

# tabs
tab_control = ttk.Notebook(window)
tab_currency = ttk.Frame(tab_control)
tab_temperature = ttk.Frame(tab_control)
tab_distance = ttk.Frame(tab_control)

tab_control.add(tab_currency, text='Currency')
tab_control.add(tab_temperature, text='Temperature')
tab_control.add(tab_distance, text='Distance')

tab_control.pack(expand=True, fill='both')

# currency tab
# 1) header with the currency types
header_currency = ttk.Frame(tab_currency)
combobox_currency_from_value = ttk.StringVar()
combobox_currency_to_value = ttk.StringVar()
combobox_currency_from = ttk.Combobox(header_currency, textvariable=combobox_currency_from_value, state='readonly', values=CURRENCY_UNITS_LIST)
combobox_currency_from.current(0)
combobox_currency_to =  ttk.Combobox(header_currency, textvariable=combobox_currency_to_value, state='readonly', values=CURRENCY_UNITS_LIST)
combobox_currency_to.current(1)
combobox_currency_from.pack(side='left', padx=10, expand=True, fill=tk.BOTH)
button_swap_currencies = ttk.Button(header_currency, text='>',
command=swap_currencies)
button_swap_currencies.pack(side='left', padx=10)
combobox_currency_to.pack(side='left', padx=10, expand=True, fill=tk.BOTH)
header_currency.pack(fill=tk.X, expand=True, )

# 2) user entry
input_currency_frame = ttk.Frame(tab_currency)
input_currency_value = ttk.StringVar()
input_currency = ttk.Entry(input_currency_frame, textvariable=input_currency_value).pack(side='left', padx = 10, fill=tk.BOTH, expand=True)
button_convert_currency = ttk.Button(input_currency_frame, text='Convert', command=convert_currency).pack(side='left', padx=10)
input_currency_frame.pack(expand=True, fill=tk.X)

# 3) converted value
converted_currency_value = ttk.StringVar()
ttk.Label(
    tab_currency, 
    textvariable=converted_currency_value, 
    font='Calibri 25 bold'
).pack(anchor=tk.CENTER)

# temperature tab
# 1) header with the temperature types
header_temperature = ttk.Frame(tab_temperature)
combobox_temperature_from_value = ttk.StringVar()
combobox_temperature_to_value = ttk.StringVar()
combobox_temperature_from = ttk.Combobox(header_temperature, textvariable=combobox_temperature_from_value, state='readonly', values=TEMPERATURE_UNITS_LIST)
combobox_temperature_from.current(0)
combobox_temperature_to =  ttk.Combobox(header_temperature, textvariable=combobox_temperature_to_value, state='readonly', values=TEMPERATURE_UNITS_LIST)
combobox_temperature_to.current(1)
combobox_temperature_from.pack(side='left', padx=10, expand=True, fill=tk.BOTH)
button_swap_currencies = ttk.Button(header_temperature, text='>', command=swap_temperatures)
button_swap_currencies.pack(side='left', padx=10)
combobox_temperature_to.pack(side='left', padx=10, expand=True, fill=tk.BOTH)
header_temperature.pack(fill=tk.X, expand=True, )

# 2) user entry
input_temperature_frame = ttk.Frame(tab_temperature)
input_temperature_value = ttk.StringVar()
input_temperature = ttk.Entry(input_temperature_frame, textvariable=input_temperature_value).pack(side='left', padx = 10, fill=tk.BOTH, expand=True)
button_convert_temperature = ttk.Button(input_temperature_frame, text='Convert', command=convert_temperature).pack(side='left', padx=10)
input_temperature_frame.pack(expand=True, fill=tk.X)

# 3) converted value
converted_temperature_value = ttk.StringVar()
ttk.Label(
    tab_temperature, 
    textvariable=converted_temperature_value, 
    font='Calibri 25 bold'
).pack(anchor=tk.CENTER)


# distance tab
# 1) header with the distance types
header_distance = ttk.Frame(tab_distance)
combobox_distance_from_value = ttk.StringVar()
combobox_distance_to_value = ttk.StringVar()
combobox_distance_from = ttk.Combobox(header_distance, textvariable=combobox_distance_from_value, state='readonly', values=DISTANCE_UNITS_LIST)
combobox_distance_from.current(0)
combobox_distance_to =  ttk.Combobox(header_distance, textvariable=combobox_distance_to_value, state='readonly', values=DISTANCE_UNITS_LIST)
combobox_distance_to.current(1)
combobox_distance_from.pack(side='left', padx=10, expand=True, fill=tk.BOTH)
button_swap_currencies = ttk.Button(header_distance, text='>', command=swap_distances)
button_swap_currencies.pack(side='left', padx=10)
combobox_distance_to.pack(side='left', padx=10, expand=True, fill=tk.BOTH)
header_distance.pack(fill=tk.X, expand=True, )

# 2) user entry
input_distance_frame = ttk.Frame(tab_distance)
input_distance_value = ttk.StringVar()
input_distance = ttk.Entry(input_distance_frame, textvariable=input_distance_value).pack(side='left', padx = 10, fill=tk.BOTH, expand=True)
button_convert_distance = ttk.Button(input_distance_frame, text='Convert', command=convert_distance).pack(side='left', padx=10)
input_distance_frame.pack(expand=True, fill=tk.X)

# 3) converted value
converted_distance_value = ttk.StringVar()
ttk.Label(
    tab_distance, 
    textvariable=converted_distance_value, 
    font='Calibri 25 bold'
).pack(anchor=tk.CENTER)

# ~~ Loop ~~
window.mainloop()