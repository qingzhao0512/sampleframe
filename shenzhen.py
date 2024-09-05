'''
Author: qingzhao0512 qingzhao0512@gmail.com
Date: 2024-09-05 11:52:21
LastEditors: qingzhao0512 qingzhao0512@gmail.com
LastEditTime: 2024-09-05 15:57:01
FilePath: \sampleframe\shenzhen.py
Description: 深圳民营诊所+抽样框爬取
'''

import requests
import pandas as pd
import json
import os


# 设置高德API信息
api_key = os.getenv('uspcpm_gaode_apikey')  # 使用环境变量 uspcpm_gaode_apikey
city = '深圳'  # 查询城市
keywords = ['诊所', '门诊部']  # 搜索关键字


# POI的全称是Point of Interest，在地理信息系统（GIS）和数字地图应用中，POI表示地图上具有特定意义和价值的位置
def fetch_poi_data(keyword, city, api_key):
    base_url = 'https://restapi.amap.com/v3/place/text'       # 高德API的基础URL，用于发送地点查询请求。
    results = []
    page = 1

    while True:                                           # 循环发送API请求，使用分页的方式获取所有结果
        params = {
            'key': api_key,
            'keywords': keyword,
            'city': city,
            'output': 'JSON',
            'offset': 20,
            'page': page
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        # 打印 API 响应内容以进行调试
#        print(f"API Response for page {page}: {data}")

        # 检查 API 响应状态
        if data['status'] != '1':                       # 检查API响应状态。如果状态不为‘1’，表示请求失败或有错误，输出错误信息并停止循环。
            print(
                f"Error: API returned status {data['status']} with info: {data.get('info')}")
            break

        if data['pois']:
            results.extend(data['pois'])
            page += 1
            if len(data['pois']) < 20:
                break
        else:
            break

    return results


def main():
    all_results = []
    results_count = {}  # 用于存储每个关键词的结果数量

    for keyword in keywords:
        # 对keywords里每个关键词进行提取，并打印当前正在提取的关键词。
        print(f"Fetching data for keyword: {keyword}")
        data = fetch_poi_data(keyword, city, api_key)
        # 将结果扩展到all_results列表中。
        all_results.extend(data)
        # 记录每个关键词对应的结果数量
        results_count[keyword] = len(data)

    # 检查all_results是否获取到任何数据
    if not all_results:
        print(
            "No data was retrieved. Please check the API key, keywords, and other settings.")
        return

    # 将数据转换为 DataFrame
    df = pd.DataFrame(all_results)

    # 打印所有列的名称
#    print("Available columns in the data:", df.columns.tolist())

    # 只打印JSON格式的第一个条目
    print("JSON格式数据的第一个条目:")
    # all_results是一个字典格式的列表，json.dumps()函数将字典转换为JSON格式的字符串，并使用indent参数设置缩进为4个空格，ensure_ascii=False参数确保非ASCII字符被正确显示。
    print(json.dumps(all_results[0], indent=4, ensure_ascii=False))

    # 如果你仍想保存完整数据，可以将数据导出到CSV
    df.to_csv('shenzhen_medical_clinics_full.csv',
              index=False, encoding='utf-8-sig')
    print("完整数据已成功导出到shenzhen_medical_clinics_full.csv文件中！")

    # 打印每个关键词对应的POI条目数
    print("\n每个关键词对应的POI条目数量:")
    for keyword, count in results_count.items():
        print(f"关键词 '{keyword}': {count} 条数据")


print(f"API Key from environment: {api_key}")

if __name__ == "__main__":
    main()
