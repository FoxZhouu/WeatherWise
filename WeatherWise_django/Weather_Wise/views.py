import requests
from django.shortcuts import render
from .data import load_city_codes  # 导入 load_city_codes 函数

def get_weather(request):
    # 用户输入的城市，可以通过 GET 参数获取
    place = request.GET.get('place', '佛山市')  # 默认值为'佛山'

    # 加载城市代码数据
    city_codes, city_location = load_city_codes('Weather_Wise/citycode.xlsx')

    # 获取城市编码和经纬度
    city_code = city_codes.get(place.strip(), '440600')  # 默认值为佛山（440600）
    location = city_location.get(place.strip())  # 获取经纬度信息
    city_longitude = location.get('longitude', '')
    city_latitude = location.get('latitude', '')

    # API 基本信息
    api_key = "13ff1bb0a5314d54676329fcc7beff1f"  # 高德 API Key
    url = "https://restapi.amap.com/v3/weather/weatherInfo?"
    static_map_url = "https://restapi.amap.com/v3/staticmap?"

    # 初始化天气数据
    live_weather_data = {}
    forecast_weather_data = []
    static_map_image_url = ""

    try:
        # 获取实时天气数据
        live_params = {
            "key": api_key,
            "city": city_code,  # 城市编码
            "extensions": "base"  # 获取实时天气数据
        }
        live_response = requests.get(url, params=live_params)

        if live_response.status_code == 200:
            live_data = live_response.json()
            if live_data['status'] == '1' and 'lives' in live_data:
                live_weather_data = live_data['lives'][0]
            else:
                live_weather_data = {"error": "无法获取实时天气数据"}
        else:
            live_weather_data = {"error": "无法获取实时天气数据"}

        # 获取天气预报数据
        forecast_params = {
            "key": api_key,
            "city": city_code,  # 城市编码
            "extensions": "all"  # 获取天气预报数据
        }
        forecast_response = requests.get(url, params=forecast_params)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            if forecast_data['status'] == '1' and 'forecasts' in forecast_data:
                # 解析预报数据，获取未来几天的天气预报
                forecast_weather_data = forecast_data['forecasts'][0]['casts']
            else:
                forecast_weather_data = {"error": "无法获取天气预报数据"}
        else:
            forecast_weather_data = {"error": "无法获取天气预报数据"}

        # 如果有经纬度，调用高德静态地图 API 生成地图
        if city_longitude and city_latitude:
            static_map_image_url = f"{static_map_url}location={city_longitude},{city_latitude}&zoom=10&size=1024*560&key={api_key}"

    except Exception as e:
        live_weather_data = {"error": f"请求实时天气数据时出错: {str(e)}"}
        forecast_weather_data = {"error": f"请求天气预报数据时出错: {str(e)}"}

    # 传递今天+后三天天气数据
    forecast_days = forecast_weather_data[0:4] if isinstance(forecast_weather_data, list) else []

    # 提取温度数据用于图表绘制
    days = [day['date'] for day in forecast_days]
    day_temps = [day['daytemp'] for day in forecast_days]
    night_temps = [day['nighttemp'] for day in forecast_days]

    # 渲染模板并传递天气数据和图表数据
    return render(request, 'weather.html', {
        'live_weather': live_weather_data,
        'forecast_weather': forecast_days,
        'place': place,  # 只传递城市名称
        'static_map_image_url': static_map_image_url,  # 静态地图 URL
        'days': days,  # 传递日期数据
        'day_temps': day_temps,  # 传递白天气温数据
        'night_temps': night_temps,  # 传递夜间气温数据
    })

def contact(request):
    return render(request, 'contact.html')


def live_cameras(request):
    return render(request, 'live-cameras.html')


def news(request):
    return render(request, 'news.html')


def photos(request):
    return render(request, 'photos.html')


def single(request):
    return render(request, 'single.html')
