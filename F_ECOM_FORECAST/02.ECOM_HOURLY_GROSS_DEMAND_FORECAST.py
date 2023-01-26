import warnings
import itertools
import sys
import pandas as pd
import statsmodels.api as smf
import pyexasol
from datetime import timedelta
from statsmodels.tsa.arima_model import ARIMA

dsn = sys.argv[1]
schema = sys.argv[2]
user = sys.argv[3]
password = sys.argv[4]
ecom_shop = sys.argv[5]

# create connection to EXASOL
CONNECTION = pyexasol.connect(dsn=dsn,
                              schema=schema,
                              user=user,
                              password=password,
                              encryption=True,
                              compression=True)

# Prepare empty tables
CONNECTION.execute("DELETE FROM STG_ECOM_FORECAST WHERE ECOM_SHOP_ID = " + str(ecom_shop) + ";")

# get data
st = CONNECTION.execute("SELECT DATE_ID, HOUR_ID, GROSS_AMNT FROM ECOM_FORECAST_DATA_TRAIN WHERE ECOM_SHOP_ID = " + str(ecom_shop) + " ORDER BY 1, 2;")
df = pd.DataFrame(data=st.fetchall(), columns=['DATE_ID', 'HOUR_ID', 'GROSS_AMNT'])
df['DATE_ID'] = pd.to_datetime(df.DATE_ID) + df.HOUR_ID.astype('timedelta64[h]')
df.drop('HOUR_ID', inplace=True, axis=1)
df.set_index('DATE_ID', inplace=True)
df.index.freq = pd.Timedelta('1h')

start = str(max(df.index)).split()[0]
end = str(max(df.index) + timedelta(days=2)).split()[0]
CONNECTION.close()

# rename variable
df.columns = ['GROSS_AMNT']
df = df.astype(int)

# Define the p, d and q parameters
# In our example, we only take values between 0 and 2 to make the computation faster
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 24) for x in list(itertools.product(p, d, q))]

# parameters AIC
warnings.filterwarnings("ignore")  # specify to ignore warning messages
i = 0
AIC = []
SARIMAX_model = []
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            i += 1
            print('The iteration', i)
            print('length of pdq', len(pdq))
            print('length of seasonalpdq', len(seasonal_pdq))
            mod = smf.tsa.statespace.SARIMAX(df,
                                             order=param,
                                             seasonal_order=param_seasonal,
                                             enforce_stationarity=False,
                                             enforce_invertibility=False)

            results = mod.fit()

            # print('SARIMAX{}x{} - AIC:{}'.format(param, param_seasonal, results.aic), end='\r')
            AIC.append(results.aic)
            SARIMAX_model.append([param, param_seasonal])
        except:
            continue

# Fitting the SARIMAX-Mode
mod = smf.tsa.statespace.SARIMAX(df,
                                 order=SARIMAX_model[AIC.index(min(AIC))][0],
                                 seasonal_order=SARIMAX_model[AIC.index(min(AIC))][1],
                                 enforce_stationarity=False,
                                 enforce_invertibility=False)

results = mod.fit()

# prediction
# start = str(datetime.today() - timedelta(days=1)).split()[0]
# end = str(datetime.today() + timedelta(days=1)).split()[0]

pred = results.get_prediction(start=pd.to_datetime(start), end=pd.to_datetime(end), dynamic=False)
# pred = results.get_prediction(start=pd.to_datetime('2020-07-11'), dynamic=False)
pred_ci = pred.conf_int()

forecast = pred.predicted_mean
# forecast.head()
df = forecast.reset_index()

# convert to string
df['DATE_ID'] = df['index'].astype("string")
df['GROSS_AMNT'] = df[0].astype(str)
df['GROSS_AMNT'] = df['GROSS_AMNT'].astype("string")

CONNECTION = pyexasol.connect(dsn=dsn,
                              schema=schema,
                              user=user,
                              password=password,
                              encryption=True,
                              compression=True)
# write to exasol
for index, row in df.iterrows():
    sql = "INSERT INTO STG_ECOM_FORECAST VALUES ('" + row['DATE_ID'] + "','" + row['GROSS_AMNT'] + "','" + str(ecom_shop) + "');"
    CONNECTION.execute(sql)

CONNECTION.close()
