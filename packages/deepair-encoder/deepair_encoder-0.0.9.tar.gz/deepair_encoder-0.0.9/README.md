## Deep Air Encoder

This package is used for encoding data fields for machine compliant dataframes.

## Package structure

`deepair_encoder`

├── encoder.py
├── __init__.py
└── utils
    ├── encoder_tools.py
    ├── __init__.py
    ├── logger.py
    └── splitters.py

1 directory, 6 files

## Dependencies

**Note**: The following python3 packages are necessary for this package to run:

* numpy
* scipy
* pandas
* sklearn
* tabulate
* tqdm

## Function Declarations

Here are the signatures for the functions in the package that can be used for deepair-dev.

### encoder.py

Below are the functions that can be accessed by importing this module as `from deepair_encoder.encoder import <function_name>`.

`encode_username`:
```
def encode_username(df, drop_field=True):
    '''
        Username one-hot encoder.
        inputs:
            df: Dataframe which have username column (pandas df series)
            drop_field: a flag if the usename column should be dropped or not after encoding (bool)
        return:
            df: Dataframe which have only username indicator [0/1] (pandas df series)
    '''
```

`encode_discounts`:
```
def encode_discounts(df, drop_field=True):
    '''
        Discounts encoder.
        inputs:
            df: dataframe which has discounts column (pandas df series)
            drop_field: a flag if the discounts column should be dropped or not after encoding (bool)
        return:
            df: a dataframe with 3 new columns 'PROMOCODE', 'RES', 'LFG' and discounts droped if drop_field = True
    '''
```

`minmax_score`:
```
def minmax_score(df, fields, keyval=['requestid', 'direction_onward'], drop_field=True, verbose=True):
    '''
        scorer function to normalize from 0-1 inversely to the value.
        inputs:
            df: Dataframe which contains fields (pandas df series)
            fields: Dataframe columns on which the score is calculated (list)
            keyval: Group the data by this key values (list)
            drop_field: Indicator to replace fields by new scored fields (bool)
            verbose: Progress bar indicator (bool)
        return:
            field: Dataframe with a score for totalprice relative to whole requestid-direction, by index, by faregroup  (pandas df series)
    '''
```

`minmax_normalize`:
```
def minmax_normalize(df, fields, keyval=['requestid', 'direction_onward'], drop_field=True, verbose=True):
    '''
        normalizer function to normalize from 0-1 proportional to the value.
        inputs:
            df: Dataframe which contains fields (pandas df series)
            fields: Dataframe columns on which the normalication is calculated (list)
            keyval: Group the data by this key values (list)
            drop_field: Indicator to replace fields by normalized new fields (bool)
            verbose: Progress bar indicator (bool)
        return:
            field: Dataframe with a score for totalprice relative to whole requestid-direction, by index, by faregroup  (pandas df series)
    '''
```

`encode_totalprice`:
```
def encode_totalprice(df):
    '''
        total price encoder.
        inputs:
            df: Dataframe which have totalprice and totaltaxes column (pandas df series)
        return:
            df: Dataframe with a score for totalprice relative to whole requestid-direction, by index, by faregroup  (pandas df series)
    '''
```

`encode_bookingid`:
```
def encode_bookingid(df):
    '''
        Bookingid flag one-hot encoder.
        inputs:
            df: Dataframe which have Bookingid column (pandas df series)
        return:
            df: Dataframe which have only Bookingid indicator [0/1] (pandas df series)
    '''
```

`encode_faregroup`:
```
def encode_faregroup(raw_file, df, verbose=False):
    '''
        Faregroup encoder.
        inputs:
            raw_file: raw_file location where the faregroup_definition is available
            df: Dataframe which have faregroup column (pandas df series)
            verbose: Optional, if more detailed log is needed
        return:
            field: Dataframe with extra fields with faregroup attributes [-1/0/1] (pandas df series)
            Note: -1 = not available, 0 = available for a fee, 1 = available for free (at no charge)
    '''
```

`encode_datetime`:
```
def encode_datetime(df, field, verbose=False):
    '''
        Datetime encoder.
        inputs:
            df: Dataframe which have 'field' column (pandas df series)
            field: the field that has to be encoded
        return:
            df: Dataframe with 6 ecoded values capturing TOD, DOW and WOY
    '''
```

`encode_advanced_purchase`:
```
def encode_advanced_purchase(df, dptr_field='departuredate', sales_field='utctimestamp'):
    '''
        advanced purchase encoder.
        inputs:
            df: Dataframe which have dptr_field and sales_field column (pandas df series)
        return:
            df: Dataframe advanced purchase column
    '''
```

`encode_los`:
```
def encode_los(df, verbose=False):
    '''
        los and trip_type encoder.
        inputs:
            df: Dataframe which have departuredate, requestid and direction column (pandas df series)
        return:
            df: Dataframe los and trip_type encodes column
    '''
```

`encode_airports`:
```
def encode_airports(df, fields, reference_file_path, verbose=True):
    '''
        encode the airports.
        inputs:
            df                      : Dataframe which have airports (pandas df series)
            fields                  : list of fields that you want to run this
                                        function on (list)
            reference_file_path     : path to the codes file (string)
            verbose                 : Indicator for progress bar (bool)
        return:
            df: Dataframe encoded with airports values
    '''
```

`encode_city`:
```
def encode_city(df, fields, reference_file_path, verbose=True):
    '''
        encode the airports.
        inputs:
            df                      : Dataframe which have city (pandas df series)
            fields                  : list of fields that you want to run this
                                        function on (list)
            reference_file_path     : path to the codes file (string)
            verbose                 : Indicator for progress bar (bool)
        return:
            df: Dataframe encoded with airports values
    '''
```

### utils

This subpackage contains tools a level lower than `encoder` module i.e. those modules that are used by encoder.

#### encoder_tools

Below are the functions that can be accessed by importing this module as `from deepair_encoder.utils.encoder_tools import <function_name>`.

`one_hot_encoder`:
```
def one_hot_encoder(df, fields, fields_drop=True, verbose=True, classes=None):
    '''
        Converts the fields into one hot encoding.
        inputs:
            df: Dataframe containing all those fields (pandas df)
            fields: Dataframe columns that you want to convert to one hot (string)
            verbose: Indicator for progress bar (bool)
            classes: Dictionary for the desired columns (dict)
        return:
            df: updated dataframe (pandas df)
    '''
```

`integer_encoder`:
```
def integer_encoder(df, fields, verbose=True):
    '''
        Converts the fields into integer encoding.
        inputs:
            df: Dataframe containing all those fields (pandas df)
            fields: Dataframe columns that you want to convert to one hot (string)
            verbose: Indicator for progress bar (bool)
        returns:
            df: updated dataframe (pandas df)
    '''
```

`get_wom`:
```
def get_wom(field):
    '''
        Function for week of the month.
        inputs:
            field: Dataframe column which have timestamp (pandas df series)
        return:
            field: Dataframe column which have wom (pandas df series)
    '''
```

`get_dow`:
```
def get_dow(field):
    '''
        Function for day of the week.
        inputs:
            field: Dataframe column which have timestamp (pandas df series)
        return:
            field: Dataframe column which have dow (pandas df series)
    '''
```

`get_month`:
```
def get_month(field):
    '''
        Function for month.
        inputs:
            field: Dataframe column which have timestamp (pandas df series)
        return:
            field: Dataframe column which have only month (pandas df series)
    '''
```

`get_year`:
```
def get_year(field):
    '''
        Function for year.
        inputs:
            field: Dataframe column which have timestamp (pandas df series)
        return:
            field: Dataframe column which have only year (pandas df series)
    '''
```

`obj2num`:
```
def obj2num(df, fields, verbose=True):
    '''
        Converts the fields into numeric from obj data type.
        inputs:
            df: Dataframe containing all those fields (pandas df)
            fields: Dataframe columns that you want to convert to numeric (string)
            verbose: Indicator for progress bar (bool)
        returns:
            df: updated dataframe (pandas df)
    '''
```

#### logger

Below are the functions that can be accessed by importing this module as `from deepair_encoder.utils.logger import <function_name>`.

`unique_stats`:
```
def unique_stats(df):
```

`_log_with_timestamp`:
```
def _log_with_timestamp(message):
    '''
        prints message on console
        input :
            message     : msg to print (string)
    '''
```

#### splitters

Below are the functions that can be accessed by importing this module as `from deepair_encoder.utils.splitters import <function_name>`.

`type_splitter`:
```
def type_splitter(data, keys=['passengertypes'], newheadings=[['ADT', 'CHD', 'INF']]):
    '''
        Split the column (need to make it more generic).
        inputs:
            data: dataframe which contain this column (pd dataframe)
            keys: list of column fields to split(list)
            newheadings: list of list for header columns in keys (list)
        returns:
            data: updated dataframe (pandas df)
    '''
```

`split_datewise`:
```
def split_datewise(df, directory='', postfix='', mode='w'):
    '''
        Split a Dataframe according to dates in UTC-Timestamp:

        input :-
            DF          : dataframe which contain this column (pd dataframe)
            directory   : path to the target directory (string)
            postfix     : any postfix you want to add (string)
            mode        : writing mode ('w':writing, 'a': append)
    '''
```

