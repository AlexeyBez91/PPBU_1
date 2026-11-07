from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests



def update_base_label(event):
    code = base_combobox.get()
    name = currencies[code][0]
    base_label.config(text=name)


def exchange():
    base_code = base_combobox.get().strip()

    name, coin_id = currencies[base_code]

    try:
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd',
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        info = data[coin_id]
        price = info['usd']

        mb.showinfo(
            f'Курс {name}',
            f'Стоимость 1 {name} ({base_code})\n'
            f'= ${price:,.6f}\n'
        )

    except Exception as er:
        mb.showerror('Ошибка', er)


currencies = {
    'BTC':        ('Bitcoin',           'bitcoin'),
    'ETH':        ('Ethereum',          'ethereum'),
    'USDT':       ('Tether',            'tether'),
    'BNB':        ('Binance Coin',      'binancecoin'),
    'XRP':        ('Ripple',            'ripple'),
    'USDC':       ('USD Coin',          'usd-coin'),
    'SOL':        ('Solana',            'solana'),
    'TRX':        ('TRON',              'tron'),
    'FIGR_HELOC': ('Figure Heloc',      'figure-heloc'),
    'STETH':      ('Lido Staked Ether', 'staked-ether'),
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
