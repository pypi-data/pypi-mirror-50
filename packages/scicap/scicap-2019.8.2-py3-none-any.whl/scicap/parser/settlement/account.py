def parse_balance(df):
    balance = 0.0
    for i in range(len(df)):
        if df.iloc[i, 5] == '客户权益':
            balance = df.iloc[i, 7]
            break
    return balance


def parse_margin(df):
    margin = 0.0
    for i in range(len(df)):
        if df.iloc[i, 5] == '保证金占用':
            margin = df.iloc[i, 7]
            break
    return margin


def parse_commission(df):
    commission = 0.0
    for i in range(len(df)):
        if df.iloc[i, 0] == '当日手续费':
            commission = df.iloc[i, 2]
            break
    return commission


def parse_deposit(df):
    deposit = 0.0
    for i in range(len(df)):
        if df.iloc[i, 0] == '当日存取合计':
            deposit = df.iloc[i, 2]
            break
    return deposit
