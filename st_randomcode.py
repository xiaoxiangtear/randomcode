## 生成不重复的随机码
import sqlite3
import random
import pandas as pd
import streamlit as st

## 生成单个随机码
def generate_numeric_code(length=6):
    digits = '0123456789'
    for t in range(65, 91):
        digits += chr(t)
        digits += chr(t+32)

    numeric_code = ''.join(random.choice(digits) for _ in range(length))
    return numeric_code

def main(digits):

    c = generate_numeric_code(digits)

    # 先判断是否已经存在该位数的随机码
    db_name = r'codes.db'  # 数据库名
    tb_name = f'digits-{digits}'  # 表名
    sql_table = f'create table `digits-{digits}` (`code` varchar(20),  primary key(`code`))'

    # 连接到数据库（本地先手动建好）
    data_path = db_name
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    # 创建表:
    try:
        #表还不存在
        cursor.execute(sql_table)
        conn.commit()  # 涉及写操作要注意提交

        sql_insert = f'replace into `digits-{digits}` (`code`) values (?)'
        cursor.execute(sql_insert, [c])
        conn.commit()  # 涉及写操作要注意提交

        return c
    except:
        print('表`{}`已存在'.format(tb_name))
        code_df = pd.read_sql(f'select * from `digits-{digits}`', con=conn)
        code_lt = code_df['code'].to_list()
        while True:
          c2 = generate_numeric_code(digits)
          if not c2 in code_lt:
            sql_insert = f'replace into `digits-{digits}` (`code`) values (?)'
            cursor.execute(sql_insert, [c])
            conn.commit()  # 涉及写操作要注意提交
            return c2
          else:
            print(f'随机码{c2}已存在，请再生成一次！')


if __name__ == '__main__':

    # digits = 3
    # code = main(digits)

    digits = st.selectbox(label='digits', options=range(2,11))
    if st.button('生成'):
        code = main(digits)
        st.write(f'随机码：{code}')