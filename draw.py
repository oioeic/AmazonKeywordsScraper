import argparse
import matplotlib.pyplot as plt

from db import db
from src.utils import load_keywords
from src.models.product import ProductORM

timelist = []
ranklist = []
sps_timelist = []
sps_ranklist = []

def getdata(keyword:str,asin:str):
    select = ProductORM.select().where(
        (ProductORM.keyword==keyword) &
        (ProductORM.product_id==asin))

    for res in select:
        dt = res.dt.strftime( '%c' )

        if(res.rank_type == 'organic'):
            timelist.append(dt)
            ranklist.append((res.page_number-1) * 15 + res.rank)
        else:
            sps_timelist.append(dt)
            sps_ranklist.append((res.page_number-1) * 5 + res.rank)
           
def plotdata(keyword:str,asin:str):
    plt.plot(timelist,ranklist,label=f'{asin} {keyword}自然排名')
    plt.plot(sps_timelist,sps_ranklist,label=f'{asin} {keyword}广告排名')
    plt.title('亚马逊排名')
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.xticks(rotation=30)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Amazon Keywords Rank Argparser!")
    parser.add_argument('--keyword', type=str, help='keyword,like:camera')
    parser.add_argument('--asin', type=str, help='asin,Ten Char and Digital,like:B0BXRMLJCM')

    args = parser.parse_args()
    if args.keyword:
        keyword_list = args.keyword.split(',')
    else:
        keyword_list = load_keywords('res/keywords.txt')

    if args.asin:
        asin_list = args.asin.split(',')
    else:
        asin_list = load_keywords('res/asins.txt')

    if not db.table_exists('productorm'):
        print(f'productorm table is not exist, please run main.py first!')

    for keyword in keyword_list:
        for asin in asin_list:
            getdata(keyword,asin)
            plotdata(keyword,asin)
