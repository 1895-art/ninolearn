import matplotlib.pyplot as plt
import numpy as np
from keras.layers import LSTM, GRU, SimpleRNN, Dense

from ninolearn.learn.rnn import Data, RNNmodel
from ninolearn.plot.evaluation import (plot_explained_variance,
                                       plot_correlations)

pool = {'c2_air': ['network_metrics', 'fraction_clusters_size_2', 'air_daily',
                   'anom', 'NCEP'],
        'c3_air': ['network_metrics', 'fraction_clusters_size_3', 'air_daily',
                   'anom', 'NCEP'],
        'c5_air': ['network_metrics', 'fraction_clusters_size_5', 'air_daily',
                   'anom', 'NCEP'],
        'c2_ssh': ['network_metrics', 'fraction_clusters_size_2', 'sshg',
                   'anom', 'GODAS'],
        'tau': ['network_metrics', 'global_transitivity', 'air_daily', 'anom',
                'NCEP'],
        'C': ['network_metrics', 'avelocal_transmissivity', 'air_daily',
              'anom', 'NCEP'],
        'S': ['network_metrics', 'fraction_giant_component', 'air_daily',
              'anom', 'NCEP'],
        'L': ['network_metrics', 'average_path_length', 'air_daily', 'anom',
              'NCEP'],
        'H': ['network_metrics', 'hamming_distance', 'air_daily', 'anom',
              'NCEP'],
        'Hstar': ['network_metrics', 'corrected_hamming_distance', 'air_daily',
                  'anom',
                  'NCEP'],
        'nino34': [None, None, 'nino3.4M', 'anom', None],
        'wwv': [None, None, 'wwv', 'anom', None],
        'pca1': ['pca', 'pca1', 'air', 'anom', 'NCEP'],
        'pca2': ['pca', 'pca2', 'vwnd', 'anom', 'NCEP'],
        'pca3': ['pca', 'pca2', 'uwnd', 'anom', 'NCEP'],
        }

window_size = 4
lead_time = 6

data_obj = Data(label_name="nino34", data_pool_dict=pool,
                window_size=window_size, lead_time=lead_time,
                startdate='1981-01', train_frac=0.67)

data_obj.load_features(['nino34', 'wwv', 'c2_ssh'
                        #'pca1', 'pca2', 'pca3',
                        # 'c3_air', 'c5_air' ,'c2_air',
                        #'S', 'H', 'tau', 'C', 'L'
                        ])

model = RNNmodel(data_obj, Layers=[SimpleRNN,SimpleRNN], n_neurons=[32,8], Dropout=0.2,
                 lr=0.01, epochs=500, batch_size=2, es_epochs=20, verbose=1)

model.fit()
model.predict()

trainRMSE, trainNRMSE = model.get_scores('train')
testRMSE, testNRMSE = model.get_scores('test')
shiftRMSE, shiftNRMSE = model.get_scores('shift')

print('Train Score: %.2f MSE, %.2f NMSE' % (trainRMSE**2, trainNRMSE))
print('Test Score: %.2f MSE, %.2f NMSE' % (testRMSE**2, testNRMSE))
print('Shift Score: %.2f MSE, %.2f NMSE' % (shiftRMSE**2, shiftNRMSE))

# %%

plt.close("all")
model.plot_history()
model.plot_prediction()

plot_explained_variance(model.Data.testYorg, model.testPredict[:, 0], model.testYtime)
plt.title(f"Lead time: {model.Data.lead_time} month")

#plot_correlations(model.Data.testYorg, model.testPredict[:, 0], model.testYtime)
