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

        label_res.config(text=f'Курс {name}\n '
                              f'Стоимость 1 {name} ({base_code})\n '
                              f'${price:,.4f}\n')

    except Exception as er:
        label_res.config(text=f'Ошибка: {er}')


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

image = 'ico.ico'
window = Tk()
window.title('Курс криптовалюты к доллару США')

w = window.winfo_screenwidth()
h = window.winfo_screenheight()
w2 = w // 2 - 185
h2 = h // 2 - 110
window.geometry(f'370x220+{w2}+{h2}')

window.configure(background='white')
window.iconbitmap(image)

label = Label(text='Запрашиваемая криптовалюта: ', background='white')
label.pack()
base_combobox = ttk.Combobox(window, values=list(currencies.keys()))
base_combobox.pack(pady=3)
base_combobox.bind('<<ComboboxSelected>>', update_base_label)
base_label = ttk.Label(background='white')
base_label.pack(pady=3)

Button(window, text='Получить курс обмена к доллару',
       command=exchange).pack(pady=5)

label_res = Label(text='', bg='white')
label_res.pack()

window.mainloop()
