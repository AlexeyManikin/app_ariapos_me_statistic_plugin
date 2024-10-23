__author__ = 'Alexey Y Manikin'

from config.config import *
from config.template import *
import traceback
from datetime import datetime
import MySQLdb


class BillParser(object):

    def __init__(self):
        self.connection = self.get_mysql_connection()

    @staticmethod
    def load_from_file(filename) -> str:
        with open(filename, 'r') as f:
            s = f.read()
        return s

    @staticmethod
    def parce_dish(text: str) -> list:
        lines = re.split(r"\n", text)
        result_line = ""
        tmp_line = ""
        for line in lines:
            if re.match(re_dish_price_format, line):
                result_line = result_line + tmp_line.replace('\n', '') + '\n' + line
                tmp_line = ""
            else:
                tmp_line = tmp_line + " " + line
        dish_result = re.findall(re_dish_format, result_line)
        dish = []
        for dr in dish_result:
            data_dish = {'name': dr[0], 'count': int(dr[1]), 'price': float(dr[2]), 'total': float(dr[3])}
            dish.append(data_dish)
        return dish

    def parce_text(self, text: str) -> list:
        result = re.findall(re_check_format, text)
        result_list = []
        for r in result:
            data = {'date': datetime.strptime(r[0], date_format2), 'bills_id': int(r[1])}

            try:
                data['bills_hash'] = re.findall(receipt_serial_number, r[2])[0]
            except:
                data['bills_hash'] = ""

            try:
                data['operator'] = re.findall(operator_name, r[2])[0]
            except:
                data['operator'] = ""

            try:
                data['operator_code'] = re.findall(operator_code, r[2])[0]
            except:
                data['operator_code'] = ""

            try:
                data['paid_by'] = re.findall(paid_by, r[2])[0]
            except:
                data['paid_by'] = ""

            try:
                data['table'] = re.findall(table_number, r[2])[0]
            except:
                data['table'] = ""

            data['dish'] = self.parce_dish(r[3])
            data['total'] = float(r[4])
            data['total_discount'] = float(r[5])
            result_list.append(data)
        return result_list

    @staticmethod
    def get_mysql_connection() -> MySQLdb.connect:
        """
        :return:
        """

        connection = MySQLdb.connect(host=MYSQL_HOST,
                                     port=MYSQL_PORT,
                                     user=MYSQL_USER,
                                     db=MYSQL_DATABASE,
                                     passwd=MYSQL_PASSWD,
                                     use_unicode=True,
                                     charset="utf8")

        connection.query("SET SESSION wait_timeout = 3600000")
        connection.query("SET @@sql_mode:=TRADITIONAL")
        connection.autocommit(True)

        return connection

    def insert_into_table(self, list_orders: list):
        try:
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            for r in list_orders:
                print('SELECT count(*) as count_in_base FROM bills WHERE bills_id = %i' % r['bills_id'])
                cursor.execute(
                    "SELECT count(*) as count_in_base FROM bills WHERE bills_id = %i" % r['bills_id'])
                count_in_base = cursor.fetchone()
                if count_in_base['count_in_base'] == 0:
                    sql = "INSERT INTO bills(date_create,bills_id,bills_hash,operator,operator_code,paied_by,table_desc,total,total_discount) "
                    sql_insert_date = """ VALUE(STR_TO_DATE('%s', '%%Y-%%m-%%d %%H:%%i:%%s'), %s, '%s', '%s', '%s', '%s', '%s', %s, %s)""" \
                                      % (r['date'],
                                         r['bills_id'],
                                         r['bills_hash'],
                                         r['operator'],
                                         r['operator_code'],
                                         r['paid_by'],
                                         r['table'],
                                         r['total'],
                                         r['total_discount'])
                    print(sql + sql_insert_date)
                    cursor.execute(sql + sql_insert_date)
                    for dr in r['dish']:
                        sql_dish = "INSERT INTO dishes(bills_id,name,item_count,price) "
                        sql_dish_insert_date = """ VALUE( %s, '%s', %s, %s)""" \
                                          % (r['bills_id'],
                                             dr['name'],
                                             dr['count'],
                                             dr['price']
                                             )
                        print(sql_dish + sql_dish_insert_date)
                        cursor.execute(sql_dish + sql_dish_insert_date)
                    self.connection.commit()

        except Exception as e:
            print(e)

    def run(self, file_name: str):
        try:
            data = self.load_from_file(file_name)
            list_data = self.parce_text(data)
            self.insert_into_table(list_data)

        except Exception as e:
            print((traceback.format_exc()))