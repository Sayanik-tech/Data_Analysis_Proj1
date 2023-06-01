import pandas as pd
import numpy as np

def preprocess(main_df,region_noc):
    ## we want only summer olympics data (Filtering data)
    main_df = main_df[main_df['Season'] == 'Summer']
    ## Merging two dataset on basis of NOC
    main_df = main_df.merge(region_noc, on='NOC', how='left')
    ## Dropping duplicates
    main_df.drop_duplicates(inplace=True)
    ## one hot encoding on medals and concatinating with main dataframe
    ## Concating the medal with main dataframe
    main_df = pd.concat([main_df, pd.get_dummies(main_df['Medal'], dtype='int')], axis=1)

    return main_df