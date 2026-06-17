import csv
import random
from datetime import datetime, timedelta

num_rows = 500000 
filename = 'loan_applications.csv'

regions = ['DE-HE', 'DE-BY', 'DE-BE', 'DE-NW', 'DE-BW']
products = ['cash_loan', 'credit_card', 'mortgage', 'auto_loan']
levels = ['low', 'medium', 'high']
statuses = ['approved', 'rejected', 'manual_review']
channels = ['mobile', 'web', 'branch', 'partner']

start_date = datetime(2026, 5, 1)

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['application_id', 'event_time', 'customer_id', 'region_code', 'product_type', 'requested_amount', 'term_months', 'credit_score', 'risk_level', 'decision_status', 'approved_amount', 'channel', 'employee_review_flag', 'processing_time_sec'])
    
    for i in range(1, num_rows + 1):
        app_id = f'app_202605_{i:06d}'
        event_time = start_date + timedelta(minutes=random.randint(0, 43200))
        cust_id = f'cust_{random.randint(10000, 99999)}'
        region = random.choice(regions)
        product = random.choice(products)
        req_amount = random.randint(10, 500) * 1000
        term = random.choice([12, 24, 36, 48, 60])
        score = random.randint(300, 850)
        risk = random.choice(levels)
        status = random.choice(statuses)
        app_amount = req_amount if status == 'approved' else 0
        channel = random.choice(channels)
        review_flag = str(status == 'manual_review').lower()
        proc_time = random.randint(1, 120)
        
        writer.writerow([app_id, event_time.strftime('%Y-%m-%d %H:%M:%S'), cust_id, region, product, req_amount, term, score, risk, status, app_amount, channel, review_flag, proc_time])

print(f"Файл {filename} сгенерирован!")
