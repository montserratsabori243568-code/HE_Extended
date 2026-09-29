import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_rows = 1000

# hay que inventar fechas en un rango como de 90 días en este ejemplo
start_date = datetime(2026, 1, 1)
dates = [start_date + timedelta(days=int(x)) for x in np.random.randint(0, 90, n_rows)]

campaigns = [f"Campana_BOFU_{i}" for i in range(1, 4)] + [f"Campana_MOFU_{i}" for i in range(1, 4)]
objectives = ['CONVERSIONS', 'OUTCOME_LEADS', 'OUTCOME_TRAFFIC']
platforms = ['facebook', 'instagram', 'audience_network']

data = []
for i in range(n_rows):
    camp = np.random.choice(campaigns)
    obj = np.random.choice(objectives)
    plat = np.random.choice(platforms)
    
    # gasto aleatorio 
    spend = round(np.random.uniform(15.0, 450.0), 2)
    
    # CPM entre $6 y $25 dólares de ejemplo
    cpm = np.random.uniform(6.0, 25.0)
    impressions = int((spend / cpm) * 1000)
    
    # CTR entre 0.8% y 3.5%
    ctr = np.random.uniform(0.008, 0.035)
    clicks = max(1, int(impressions * ctr))
    
    # la tasa de conversión según el objetivo
    conv_rate = np.random.uniform(0.02, 0.08) if obj == 'CONVERSIONS' else np.random.uniform(0.005, 0.02)
    conversions = int(clicks * conv_rate)
    
    # valor estimado p/conversión
    conv_value = round(conversions * np.random.uniform(25.0, 90.0), 2) if conversions > 0 else 0.0
    
    data.append({
        'date': dates[i].strftime('%Y-%m-%d'),
        'campaign_name': camp,
        'objective': obj,
        'publisher_platform': plat,
        'spend': spend,
        'impressions': impressions,
        'clicks': clicks,
        'conversions': conversions,
        'conversion_value': conv_value
    })

df = pd.DataFrame(data)

# estas serán las métricas calculadas falsas
df['ctr'] = (df['clicks'] / df['impressions']).round(4)
df['cpc'] = (df['spend'] / df['clicks']).round(2)
df['cpa'] = np.where(df['conversions'] > 0, (df['spend'] / df['conversions']).round(2), 0)
df['roas'] = np.where(df['spend'] > 0, (df['conversion_value'] / df['spend']).round(2), 0)

# exportamos
df.to_csv('meta_ads_fake_dataset.csv', index=False)
print("Dataset generado con éxito (1,000 filas).")