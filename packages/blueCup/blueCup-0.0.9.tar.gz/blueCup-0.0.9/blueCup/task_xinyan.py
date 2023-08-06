from typing import Any, Dict

from .celery import app


@app.task(name='async_xinyan_overdue_main', bind=True, autoretry_for=(Exception,),
          retry_kwargs={'max_retries': 3, 'countdown': 1})
def async_xinyan_overdue_main(self: Any, idcard: str,
                              id_name: str,
                              private_key_path: str,
                              url: str = 'https://api.xinyan.com/product/archive/v3/overdue',
                              phone_no: str = '',
                              bankcard_no: str = '',
                              member_id: str = '',
                              terminal_id: str = '') -> Dict:
    from muzha.xinyan.base import xinyan_overdue_main

    return xinyan_overdue_main(idcard,
                               id_name,
                               private_key_path,
                               url=url,
                               phone_no=phone_no,
                               bankcard_no=bankcard_no,
                               member_id=member_id,
                               terminal_id=terminal_id)


@app.task(name='async_xinyan_radar_main', bind=True, autoretry_for=(Exception,),
          retry_kwargs={'max_retries': 3, 'countdown': 1})
def async_xinyan_radar_main(self: Any, idcard: str,
                            id_name: str,
                            private_key_path: str,
                            url: str = 'https://api.xinyan.com/product/radar/v3/apply',
                            phone_no: str = '',
                            bankcard_no: str = '',
                            member_id: str = '',
                            terminal_id: str = '') -> Dict:
    from muzha.xinyan.base import xinyan_radar_main
    return xinyan_radar_main(idcard,
                             id_name,
                             private_key_path,
                             url=url,
                             phone_no=phone_no,
                             bankcard_no=bankcard_no,
                             member_id=member_id,
                             terminal_id=terminal_id)
