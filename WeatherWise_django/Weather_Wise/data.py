import pandas as pd

def load_city_codes(file_path):
    # 使用 pandas 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 构建城市名称和城市代码的映射字典
    city_codes = {}
    city_location = {}

    for _, row in df.iterrows():
        city_name = row['中文名'].strip()
        city_code = str(row['adcode']).strip()
        city_longitude = str(row['经度']).strip()
        city_latitude = str(row['纬度']).strip()

        if city_name and city_code:
            city_codes[city_name] = city_code
            city_location[city_name] = {"longitude": city_longitude, "latitude": city_latitude}



    return city_codes,city_location
