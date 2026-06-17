import csv
import random
from datetime import datetime, timedelta


num_rows = 350000 
filename = 'transactions_v2.csv'

regions = ['DE-HE', 'DE-BY', 'DE-BE', 'DE-NW']
campaigns = ['credit_card_offer', 'mortgage_promo', 'personal_loan']
statuses = ['answered', 'missed', 'voicemail']
responses = ['interested', 'not_interested', 'call_back_later', 'none']

start_date = datetime(2026, 5, 1)

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['call_id', 'call_time', 'client_id', 'region_code', 'campaign_type', 'call_status', 'client_response', 'duration_sec', 'follow_up_required'])
    
    for i in range(1, num_rows + 1):
        call_id = f'call_202605_{i:06d}'
        call_time = start_date + timedelta(minutes=random.randint(0, 43200)) # Размазываем по месяцу
        client_id = f'client_{random.randint(1000, 99999)}'
        region = random.choice(regions)
        campaign = random.choice(campaigns)
        status = random.choice(statuses)
        response = random.choice(responses) if status == 'answered' else 'none'
        duration = random.randint(10, 600) if status == 'answered' else 0
        follow_up = str(response == 'call_back_later').lower()
        
        writer.writerow([call_id, call_time.strftime('%Y-%m-%d %H:%M:%S'), client_id, region, campaign, status, response, duration, follow_up])

print(f"Файл {filename} успешно сгенерирован!")
