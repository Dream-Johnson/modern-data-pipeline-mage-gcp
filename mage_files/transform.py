import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    #df.info()

    df = df.drop_duplicates().reset_index(drop=True)
    df['trip_id'] = df.index
    #df.head()

    datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].reset_index(drop=True)
    datetime_dim['pick_hour']=datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pick_day']=datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pick_month']=datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pick_year']=datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pick_weekday']=datetime_dim['tpep_pickup_datetime'].dt.weekday
    #datetime_dim

    datetime_dim['drop_hour']=datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['drop_day']=datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['drop_month']=datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['drop_year']=datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['drop_weekday']=datetime_dim['tpep_dropoff_datetime'].dt.weekday
    datetime_dim['datetime_id']=datetime_dim.index
    #datetime_dim

    datetime_dim = datetime_dim[['datetime_id','tpep_pickup_datetime','pick_hour','pick_month','pick_year','pick_weekday','tpep_dropoff_datetime','drop_hour','drop_day','drop_month','drop_year','drop_weekday']]
    #datetime_dim.head(10)

    passenger_count_dim=df[['passenger_count']].reset_index(drop=True)
    passenger_count_dim['passenger_count_id']=passenger_count_dim.index
    passenger_count_dim=passenger_count_dim[['passenger_count_id','passenger_count']]
    #passenger_count_dim.head(10)

    trip_distance_dim = df[['trip_distance']].reset_index(drop=True)
    trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
    trip_distance_dim=trip_distance_dim[['trip_distance_id','trip_distance']]
    #trip_distance_dim.head(10)


    rate_code_type = {
    1:'Standard rate',
    2:'JFK',
    3:'Newark',
    4:'Nassau or Westchester',
    5:'Negotiated fare',
    6:'Group ride'
    }

    rate_code_dim=df[['RatecodeID']].reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim['rate_code_name']=rate_code_dim['RatecodeID'].map(rate_code_type)
    rate_code_dim = rate_code_dim[['rate_code_id','RatecodeID','rate_code_name']]
    #rate_code_dim.head(5)
    #df.columns



    #Pickup
    pickup_location_dim=df[['pickup_latitude','pickup_longitude']].reset_index(drop=True)
    pickup_location_dim['pickup_location_id']=pickup_location_dim.index
    pickup_location_dim=pickup_location_dim[['pickup_location_id','pickup_latitude','pickup_longitude']]
    #pickup_location_dim.head()


    #Dropoff
    drop_location_dim=df[['dropoff_longitude','dropoff_latitude']].reset_index(drop=True)
    drop_location_dim['dropoff_location_id']=drop_location_dim.index
    drop_location_dim=drop_location_dim[['dropoff_location_id','dropoff_latitude','dropoff_longitude']]
    #drop_location_dim.head()

    payment_types = {
    1:"Credit card",
    2:"Cash",
    3:"No charge",
    4:"Dispute",
    5:"Unknown",
    6:"Voided trip"
    }


    payment_type_dim = df[['payment_type']].reset_index(drop=True)
    payment_type_dim['payment_type_id']=payment_type_dim.index
    payment_type_dim['payment_type_name']=payment_type_dim['payment_type'].map(payment_types)
    payment_type_dim=payment_type_dim[['payment_type_id','payment_type','payment_type_name']]
    #payment_type_dim.head(10)

    fact_table = df.merge(passenger_count_dim, left_on='trip_id', right_on='passenger_count_id') \
             .merge(trip_distance_dim, left_on='trip_id', right_on='trip_distance_id') \
             .merge(rate_code_dim, left_on='trip_id', right_on='rate_code_id') \
             .merge(pickup_location_dim, left_on='trip_id', right_on='pickup_location_id') \
             .merge(drop_location_dim, left_on='trip_id', right_on='dropoff_location_id')\
             .merge(datetime_dim, left_on='trip_id', right_on='datetime_id') \
             .merge(payment_type_dim, left_on='trip_id', right_on='payment_type_id') \
             [['trip_id','VendorID', 'datetime_id', 'passenger_count_id',
               'trip_distance_id', 'rate_code_id', 'store_and_fwd_flag', 'pickup_location_id', 'dropoff_location_id',
               'payment_type_id', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
               'improvement_surcharge', 'total_amount']]

  
  

    return {"datetime_dim":datetime_dim,
    "passenger_count_dim":passenger_count_dim,
    "trip_distance_dim":trip_distance_dim,
    "rate_code_dim":rate_code_dim,
    "pickup_location_dim":pickup_location_dim,
    "drop_location_dim":drop_location_dim,
    "payment_type_dim":payment_type_dim,
    "fact_table":fact_table}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
