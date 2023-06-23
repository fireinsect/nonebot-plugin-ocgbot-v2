import sqlite3


class SqliteUtils:
    @staticmethod
    def dict_factory(cursor, row):
        # 将游标获取的数据处理成字典返回
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self,db_file):
        # 建立和数据库的连接
        conn = sqlite3.connect(db_file)
        # 使得查询结果以字典形式返回
        conn.row_factory = SqliteUtils.dict_factory
        # 创建游标以用于执行sql
        cursor = conn.cursor()
        return conn, cursor
