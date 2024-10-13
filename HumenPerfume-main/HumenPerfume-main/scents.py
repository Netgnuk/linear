import pandas as pd

# อ่านไฟล์ CSV
df = pd.read_csv('perfume_scent_base_middle_counts.csv')

# กรองเอาเฉพาะค่าตัวแรก
first_items = df['scents'].unique()  # แทนที่ 'Base Note' ด้วยชื่อคอลัมน์ที่คุณใช้

# สร้าง JSON
json_data = [{'scents': item} for item in first_items]

# บันทึกเป็นไฟล์ JSON
with open('scents.json', 'w', encoding='utf-8') as f:
    f.write(pd.Series(json_data).to_json(orient='records', lines=False))