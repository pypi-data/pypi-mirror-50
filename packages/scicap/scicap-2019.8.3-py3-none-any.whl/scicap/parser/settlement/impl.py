import pandas as pd
from . import account
from . import trade
from . import position


def parse_account(dir_path, broker_id, account_id, date):
    filename = f'{dir_path}/{broker_id}{account_id}_{date}.xls'
    data_df = pd.read_excel(filename, sheet_name='客户交易结算日报')

    rtn_df = pd.DataFrame(data=[['', '', '', 0.0, 0.0, 0.0]],
                          columns=['DATE', 'BROKER_ID', 'ACCOUNT_ID', 'BALANCE', 'MARGIN', 'COMMISSION'])
    rtn_df['DATE'] = date
    rtn_df['BROKER_ID'] = broker_id
    rtn_df['ACCOUNT_ID'] = account_id
    rtn_df['BALANCE'] = account.parse_balance(data_df)
    rtn_df['MARGIN'] = account.parse_margin(data_df)
    rtn_df['COMMISSION'] = account.parse_commission(data_df)
    return rtn_df


def parse_trade(dir_path, broker_id, account_id, date):
    filename = f'{dir_path}/{broker_id}{account_id}_{date}.xls'
    data_df = pd.read_excel(filename, sheet_name='成交明细')
    trade_df = trade.parse_trade_df(data_df)

    rtn_df = pd.DataFrame(columns=['DATE', 'BROKER_ID', 'ACCOUNT_ID', 'INSTRUMENT_ID', 'TRADE_ID', 'TRADE_TIME',
                                   'DIRECTION', 'HEDGE_FLAG', 'PRICE', 'LOTS', 'AMOUNT', 'OFFSET_FLAG', 'COMMISSION',
                                   'CLOSE_PROFIT'])
    rtn_df['INSTRUMENT_ID'] = trade_df.iloc[:, 0]
    rtn_df['DATE'] = date
    rtn_df['BROKER_ID'] = broker_id
    rtn_df['ACCOUNT_ID'] = account_id
    rtn_df['TRADE_ID'] = trade_df.iloc[:, 1]
    rtn_df['TRADE_TIME'] = trade_df.iloc[:, 2]

    check_flag = trade_df.iloc[:, 3].apply(lambda x: x.strip() not in ['买', '卖'])
    assert not check_flag.any()
    rtn_df['DIRECTION'] = trade_df.iloc[:, 3].apply(lambda x: 'BUY' if x.strip() == '买' else 'SELL')

    check_flag = trade_df.iloc[:, 4].apply(lambda x: x.strip() not in ['投机', '套保'])
    assert not check_flag.any()
    rtn_df['HEDGE_FLAG'] = trade_df.iloc[:, 4].apply(lambda x: 'SPECULATION' if x.strip() == '投机' else 'HEDGE')

    rtn_df['PRICE'] = trade_df.iloc[:, 5].apply(float)
    rtn_df['LOTS'] = trade_df.iloc[:, 6].apply(int)
    rtn_df['AMOUNT'] = trade_df.iloc[:, 7].apply(float)

    check_flag = trade_df.iloc[:, 8].apply(lambda x: x.strip() not in ['开', '平'])
    assert not check_flag.any()
    rtn_df['OFFSET_FLAG'] = trade_df.iloc[:, 8].apply(lambda x: 'OPEN' if x.strip() == '开' else 'CLOSE')

    rtn_df['COMMISSION'] = trade_df.iloc[:, 9].apply(float)
    rtn_df['CLOSE_PROFIT'] = trade_df.iloc[:, 10].apply(lambda x: 0 if x == '--' else int(x))
    return rtn_df


def parse_position(dir_path, broker_id, account_id, date):
    filename = f'{dir_path}/{broker_id}{account_id}_{date}.xls'
    data_df = pd.read_excel(filename, sheet_name='客户交易结算日报')
    position_df = position.parse_position_df(data_df)

    rtn_df = pd.DataFrame(columns=['DATE', 'BROKER_ID', 'ACCOUNT_ID', 'INSTRUMENT_ID', 'BUY_LOTS', 'BUY_PRICE',
                                   'SELL_LOTS', 'SELL_PRICE'])

    rtn_df['INSTRUMENT_ID'] = position_df.iloc[:, 0]
    rtn_df['DATE'] = date
    rtn_df['BROKER_ID'] = broker_id
    rtn_df['ACCOUNT_ID'] = account_id

    rtn_df['BUY_LOTS'] = position_df.iloc[:, 1]
    rtn_df['BUY_PRICE'] = position_df.iloc[:, 2]
    rtn_df['SELL_LOTS'] = position_df.iloc[:, 3]
    rtn_df['SELL_PRICE'] = position_df.iloc[:, 4]
    rtn_df.fillna(value=0, inplace=True)
    return rtn_df




