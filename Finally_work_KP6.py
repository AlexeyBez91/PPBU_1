from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests



def update_currency_label(event):
    code = target_combobox.get()
    name = currencies[code]
    target_label.config(text=name)


def update_base_label(event):
    code = base_combobox.get()
    name = currencies[code]
    base_label.config(text=name)


def update_base2_label(event):
    code = base_combobox.get()
    name = currencies[code]
    base2_label.config(text=name)


def exchange():
    target_code = target_combobox.get().strip()
    base_code = base_combobox.get().strip()
    base2_code = base2_combobox.get().strip()

    if base_code == base2_code:
        mb.showwarning('Внимание', 'Базовые валюты должны различаться!')
        return

    if target_code in (base_code, base2_code):
        mb.showwarning('Внимание', 'Целевая валюта дожна отличаться от базовых!')
        return

    if target_code and base_code and base2_code:
        try:
            response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')
            response.raise_for_status()
            data = response.json()

            response2 = requests.get(f'https://open.er-api.com/v6/latest/{base2_code}')
            response2.raise_for_status()
            data2 = response2.json()

            if target_code in data['rates'] and target_code in data2['rates']:
                exchange_rate = data['rates'][target_code]
                exchange_rate2 = data2['rates'][target_code]
                base = currencies[base_code]
                base2 = currencies[base2_code]
                target = currencies[target_code]
                mb.showinfo('Курс обмена',
                            f'Курс: {exchange_rate:.4f} {target} за 1 {base}\n'
                            f'Курс: {exchange_rate2:.4f} {target} за 1 {base2}')
            else:
                mb.showerror('Ошибка',
                             f'Валюта {target_code} не найдена')
        except Exception as er:
            mb.showerror('Ошибка', er)

    else:
        mb.showwarning('Внимание', 'Введите код валюты')


currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'JPY': 'Японская йена',
    'GBP': 'Фунт стерлингов',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'RUB': 'Российский рубль ',
    'KZT': 'Казахстанский тенге',
    'UZS': 'Узбекский сум'
}

root = Tk()
root.title('Курс обмена валют')
root.geometry('380x300')

Label(root, text='Базовая валюта №1').pack(pady=3)
base_combobox = ttk.Combobox(root, values=list(currencies.keys()))
base_combobox.pack(pady=3)
base_combobox.bind('<<ComboboxSelected>>', update_base_label)
base_label = ttk.Label()
base_label.pack(pady=3)

Label(root, text='Базовая валюта №2').pack(pady=3)
base2_combobox = ttk.Combobox(root, values=list(currencies.keys()))
base2_combobox.pack(pady=3)
base2_combobox.bind('<<ComboboxSelected>>', update_base2_label)
base2_label = ttk.Label()
base2_label.pack(pady=3)

Label(root, text='Целевая валюта').pack(pady=3)
target_combobox = ttk.Combobox(root, values=list(currencies.keys()))
target_combobox.pack(pady=3)
target_combobox.bind('<<ComboboxSelected>>', update_currency_label)
target_label = ttk.Label()
target_label.pack(pady=3)

Button(root, text='Получить курс обмена к доллару',
       command=exchange).pack(pady=5)

root.mainloop()
