import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor

# Charger vos données boursières dans un DataFrame
data = pd.read_csv('donnees_boursieres.csv')

# Assurez-vous que la colonne 'Date' est correctement formatée comme une date
data['Date'] = pd.to_datetime(data['Date'])

# Triez les données par date si ce n'est pas déjà le cas
data = data.sort_values(by='Date')

# Sélectionnez les colonnes pertinentes
data = data[['Date', 'Prix de Clôture']]

# Normalisez les données
scaler = MinMaxScaler()
data['Prix de Clôture'] = scaler.fit_transform(data['Prix de Clôture'].values.reshape(-1, 1))

# Spécifiez la période de saisonnalité (par exemple, 1 mois pour une saisonnalité mensuelle)
periode_saisonnalite = 30  # ou 20, 21, etc., en fonction de votre période de saisonnalité

# Appliquez la différenciation pour enlever la saisonnalité
data['Difference'] = data['Prix de Clôture'].diff(periods=periode_saisonnalite)
data = data.dropna()

# Divisez les données en ensembles d'entraînement et de test
X = data['Date']
y = data['Difference']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Créez une fonction pour construire le modèle LSTM
def build_lstm_model(neurons=50, dropout=0.2):
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(X_train.shape[1], 1), return_sequences=True))
    model.add(Dropout(dropout))
    model.add(LSTM(neurons, return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Créez une instance du modèle
model = KerasRegressor(build_fn=build_lstm_model, epochs=50, batch_size=32)

# Définissez les hyperparamètres à optimiser
param_grid = {
    'neurons': [50, 100],
    'dropout': [0.2, 0.3]
}

# Effectuez une recherche par grille pour trouver les meilleurs hyperparamètres
grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)
grid_result = grid.fit(X_train, y_train)

# Obtenez les meilleurs hyperparamètres
best_neurons = grid_result.best_params_['neurons']
best_dropout = grid_result.best_params_['dropout']

# Entraînez le modèle avec les meilleurs hyperparamètres
final_model = build_lstm_model(neurons=best_neurons, dropout=best_dropout)
final_model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=2)

# Effectuez des prédictions sur l'ensemble de test
y_pred = final_model.predict(X_test)

# Inversez la normalisation des prédictions
y_pred = scaler.inverse_transform(y_pred)
y_true = scaler.inverse_transform(y_test.values.reshape(-1, 1))

# Calcul du MAE
mae = mean_absolute_error(y_true, y_pred)
print(f"Mean Absolute Error (MAE): {mae}")
