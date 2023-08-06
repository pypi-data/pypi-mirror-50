def parse_trade_df(df):
    begin_index = 0
    end_index = 0
    for i in range(len(df)):
        if df.iloc[i, 0] == "合约":
            begin_index = i
        elif df.iloc[i, 0] == "合计":
            end_index = i
    assert begin_index > 0
    assert end_index > 0
    return df.iloc[begin_index + 1:end_index, 0:-1]
