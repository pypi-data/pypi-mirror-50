from functools import partial
from typing import Mapping, Any, Callable

import pandas as pd
from muzha.shuhemofang import network_triple_elements as shmf_network_triple_elements
from nezha import umongo
from nezha import utime
from nezha.aliyun.uemail import Email
from nezha.file import File
from nezha.uexcel import to_excel
from nezha.umongo import insert_one, find, find_one
from nezha.utime import strftime

from .celery import app

DB = 'third_interface'
COLLECTION = 'bill'
MONGO_HOST = '47.103.51.193'
MONGO_USERNAME = 'root'
MONGO_PWD = '*******'
_email_info = find_one({'block': 'default'},
                       'email_notification_config',
                       DB,
                       MONGO_HOST,
                       27017,
                       MONGO_USERNAME,
                       MONGO_PWD,
                       'admin')['email_info']
EMAIL = Email(_email_info['mail_user'], _email_info['mail_pass'], _email_info['sender'])
RECEIVERS = _email_info['receiver']
partial_insert_one = partial(insert_one,
                             db=DB,
                             host=MONGO_HOST,
                             port=27017,
                             username=MONGO_USERNAME,
                             password=MONGO_PWD,
                             authSource='admin')

partial_find = partial(find,
                       db=DB,
                       host=MONGO_HOST,
                       port=27017,
                       username=MONGO_USERNAME,
                       password=MONGO_PWD,
                       authSource='admin')


@app.task(name='bill_shuhemofang_network_triple_elements',
          bind=True, autoretry_for=(Exception,),
          retry_kwargs={'max_retries': 3, 'countdown': 1})
def bill_shuhemofang_network_triple_elements(self: Any,
                                             boolean_order_id: str,
                                             supplier_order_id: str,
                                             supplier_response: Mapping,
                                             call_time: str = strftime(),
                                             stored_func: Callable = partial_insert_one,
                                             supplier_uuid: str = 'shuhemofang',
                                             supplier_name: str = '数盒魔方',
                                             product_uuid: str = 'network_triple_elements',
                                             product_name: str = '运营商三要素') -> None:
    product_price = shmf_network_triple_elements.how_much_should_pay(supplier_response)
    supplier_status = True if product_price else False
    data = locals().copy()
    list(map(lambda x: data.pop(x), ('self', 'stored_func')))
    stored_func(data)


@app.task(name='bill_yesterday_count',
          bind=True, autoretry_for=(Exception,),
          retry_kwargs={'max_retries': 3, 'countdown': 1})
def bill_yesterday_count(self: Any):
    all_iter = partial_find({'call_time': umongo.yesterday}, 'bill')
    result = []
    for one_record in all_iter:
        if isinstance(one_record, dict):
            not_display_keys = {'_id', 'supplier_response', 'supplier_uuid', 'product_uuid'}
            tuple(map(lambda key: one_record.get(key) and one_record.pop(key), not_display_keys))
            result.append(one_record)
        else:
            print(f'one_record {one_record} is unexpected')
    p_columns = {
        'boolean_order_id': '布尔订单号',
        'call_time': '调用时间',
        'product_name': '产品名称',
        'product_price': '产品单价',
        'supplier_name': '供应商名称',
        'supplier_order_id': '供应商订单号',
        'supplier_status': '状态',
    }
    p_header = ('布尔订单号', '供应商订单号', '供应商名称', '产品名称', '产品单价', '调用时间', '状态')
    df = pd.DataFrame(result, columns=p_columns)
    df.rename(columns=p_columns, inplace=True)
    yesterday = utime.yesterday(precision="day")
    xlsx = File.join_path(File.this_dir(__file__), f'{yesterday}.xlsx')
    to_excel(df, xlsx, columns=p_header)
    EMAIL.send_email_attach(f'{yesterday} 供应商调用统计', '', xlsx, RECEIVERS)


if __name__ == '__main__':
    bill_yesterday_count()
