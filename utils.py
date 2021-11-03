def preprocess(df):

    # Removes missing values in the dataframe
    def remove_missing_values(df):
        df = df.dropna()

        df = df[(df['amount'] > 0)]
        for ind in df.index:
            if df['amount'][ind] == 0:

                df.drop(ind)

        return df

    # Removes outliers in fare amount
    def remove_amount_outliers(df, lower_bound, upper_bound):

        df = df[(df['amount'] > lower_bound) & (df['amount'] <= upper_bound)]
        return df

    # Changes friday with  2
    def change_friday(df):
        for ind in df.index:
            if df['week'][ind] == 'Friday':
                df['holiday'][ind] = 2

        return df

    # Adds one to holiday column
    def add_one_holiday(df):
        for ind in df.index:

            df['holiday'][ind] += 1

        return df

    # Converts day to numeric value
    def day_to_num(df):

        df['week'] = df['week'].replace('Saturday', 1)
        df['week'] = df['week'].replace('Sunday', 2)
        df['week'] = df['week'].replace('Monday', 3)
        df['week'] = df['week'].replace('Tuesday', 4)
        df['week'] = df['week'].replace('Wednesday', 5)
        df['week'] = df['week'].replace('Thursday', 6)
        df['week'] = df['week'].replace('Friday', 7)

        return df

    # Adds the average of the 7 previous days
    def add_avg(df):
        for ind in df.index:
            if ind - 7 < 0:

                h = df.iloc[0:ind + 1, 0].mean()

            else:

                h = df.iloc[ind - 7:ind + 1, 0].mean()

            df['avg'][ind] = h
        return df

    # Adds season column
    def add_season(df):
        for ind in df.index:
            if 0 < df['month'][ind] < 4:
                df['season'][ind] = 1
            elif 3 < df['month'][ind] < 7:
                df['season'][ind] = 2
            elif 6 < df['month'][ind] < 10:
                df['season'][ind] = 3
            else:
                df['season'][ind] = 4

        return df

    # Recognizes whether the day before is a holiday or not
    def add_before(df):
        for ind in df.index:
            try:
                if df['holiday'][ind + 1] > 0:
                    df['before'][ind] = 1
            except:
                continue

        return df

    # Recognizes whether we are in the first days of the month or not
    def add_beginnig(df):
        for ind in df.index:
            if 0 < df['day'][ind] < 8:
                df['beginning'][ind] = 1

        return df

    print(df.shape, "     shape")

    # Running functions
    df = add_avg(df)
    df = add_season(df)
    df = remove_missing_values(df)
    df = remove_amount_outliers(df, lower_bound=40000000, upper_bound=150000000)
    df = change_friday(df)
    df = day_to_num(df)
    df = add_one_holiday(df)
    df = add_before(df)
    df = add_beginnig(df)
    print(df.shape)
    return df
