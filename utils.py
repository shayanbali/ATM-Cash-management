def preprocess(df):
    # remove missing values in the dataframe
    def remove_missing_values(df):
        df = df.dropna()
        return df

    # remove outliers in fare amount
    def remove_fare_amount_outliers(df, lower_bound, upper_bound):
        df = df[(df['amount'] > lower_bound) & (df['fare_amount'] <= upper_bound)]
        return df

    # change friday with  2
    def change_friday(df):
        df['holiday'][(df['week'] == 'friday')].replace(2, 3)

    def day_to_num(df):
        df['week'] = df['week'].replace('Saturday', 0)
        df['week'] = df['week'].replace('Sunday', 1)
        df['week'] = df['week'].replace('Monday', 2)
        df['week'] = df['week'].replace('Tuesday', 3)
        df['week'] = df['week'].replace('Wednesday', 4)
        df['week'] = df['week'].replace('Thursday', 5)
        df['week'] = df['week'].replace('Friday', 6)

        return df
