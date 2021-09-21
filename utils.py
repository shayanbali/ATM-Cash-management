def preprocess(df):
    # remove missing values in the dataframe
    def remove_missing_values(df):
        df = df.dropna()

        for ind in df.index:
            if df['amount'][ind] == 0:
                df.drop(ind)

        return df

    # remove outliers in fare amount
    def remove_amount_outliers(df, lower_bound, upper_bound):
        df = df[(df['amount'] > lower_bound) & (df['amount'] <= upper_bound)]
        return df

    # change friday with  2
    def change_friday(df):
        for ind in df.index:
            if df['week'][ind] == 'Friday':
                df['holiday'][ind] = 2

        return df

    def add_one_holiday(df):
        for ind in df.index:
            df['holiday'][ind] += 1
        return df

    def day_to_num(df):
        df['week'] = df['week'].replace('Saturday', 1)
        df['week'] = df['week'].replace('Sunday', 2)
        df['week'] = df['week'].replace('Monday', 3)
        df['week'] = df['week'].replace('Tuesday', 4)
        df['week'] = df['week'].replace('Wednesday', 5)
        df['week'] = df['week'].replace('Thursday', 6)
        df['week'] = df['week'].replace('Friday', 7)

        return df

    def add_avg(df):
        for ind in df.index:
            if ind - 7 < 0:
                h = df.iloc[0:ind+1, 0].mean()
            else:
                h = df.iloc[ind - 7:ind+1, 0].mean()
            print(h, ind - 7)
            df['avg'][ind] = h
        return df

    df = add_avg(df)
    df = remove_missing_values(df)
    df = remove_amount_outliers(df, lower_bound=40000000, upper_bound=140000000)
    df = change_friday(df)
    df = day_to_num(df)
    df = add_one_holiday(df)
    print(df.shape)
    return df
