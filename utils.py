def preprocess(df):
    # remove missing values in the dataframe
    def remove_missing_values(df):
        df = df.dropna()
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

    def day_to_num(df):
        df['week'] = df['week'].replace('Saturday', 0)
        df['week'] = df['week'].replace('Sunday', 1)
        df['week'] = df['week'].replace('Monday', 2)
        df['week'] = df['week'].replace('Tuesday', 3)
        df['week'] = df['week'].replace('Wednesday', 4)
        df['week'] = df['week'].replace('Thursday', 5)
        df['week'] = df['week'].replace('Friday', 6)

        return df

    df = remove_missing_values(df)
    df = remove_amount_outliers(df, lower_bound=40000000, upper_bound=150000000)
    df = change_friday(df)
    df = day_to_num(df)
    print(df.shape)
    return df
