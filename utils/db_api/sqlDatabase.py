import sqlite3

from sqlite3 import Error


class Database:

    def __init__(self, path_to_db="Users.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):

        if not parameters:
            parameters = tuple()

        connection = self.connection
        cursor = connection.cursor()
        connection.set_trace_callback(logger)
        cursor.execute(sql, parameters)

        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        ids str NOT NULL,
        fullname varchar(255),
        username varchar(255),
        userWallet varchar(255),
        userBalance varchar(255),
        lastRefreshDate varchar(255),
        verificationWalletAddress varchar(255),
        verificationWalletPrivetHex int(255),
        verificationWalletPrivetSeed varchar(255),
        userTransaction varchar(255),
        verificationProcess varchar(255),
        adminRights varchar(255),
        warnings int(255),
        PRIMARY KEY (ids)
        );"""
        self.execute(sql, commit=True)

    def add_user(self,
                 ids: str,  # 0
                 fullname: str,  # 1
                 username: str = None,  # 2
                 userWallet: str = None,  # 3
                 userBalance: int = None,  # 4
                 lastRefreshDate: str = None,  # 5
                 verificationWalletAddress: str = None,  # 6
                 verificationWalletPrivetHex: float = None,  # 7
                 verificationWalletPrivetSeed: str = None,  # 8
                 userTransaction: str = None,  # 9
                 verificationProcess: str = None,  # 10
                 adminRights: int = 0,  # 11
                 warnings: int = 0):  # 12

        SQL_COMMAND = "INSERT OR IGNORE INTO Users(ids, fullname, username, userWallet, userBalance, lastRefreshDate, verificationWalletAddress, verificationWalletPrivetHex, " \
                      "verificationWalletPrivetSeed, userTransaction, verificationProcess, adminRights, warnings) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) "

        parameters = (ids,
                      fullname,
                      username,
                      userWallet,
                      userBalance,
                      lastRefreshDate,
                      verificationWalletAddress,
                      verificationWalletPrivetHex,
                      verificationWalletPrivetSeed,
                      userTransaction,
                      verificationProcess,
                      adminRights,
                      warnings)

        self.execute(SQL_COMMAND, parameters=parameters, commit=True)

    def select_all_users(self):
        SQL_COMMAND = "SELECT * FROM Users"
        return self.execute(SQL_COMMAND, fetchall=True)

    def update_user_balance(self, status, user_id):
        SQL_COMMAND = "UPDATE Users SET userBalance=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(status, user_id), commit=True)

    def select_user(self, **kwargs):
        SQL_COMMAND = "SELECT * FROM Users WHERE"
        SQL_COMMAND, parameters = self.format_args(SQL_COMMAND, kwargs)
        return self.execute(SQL_COMMAND, parameters=parameters, fetchone=True)

    def select_users(self, **kwargs):
        SQL_COMMAND = "SELECT * FROM Users WHERE"
        SQL_COMMAND, parameters = self.format_args(SQL_COMMAND, kwargs)
        return self.execute(SQL_COMMAND, parameters=parameters, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def get_all_banned_users(self,):
        SQL_COMMAND = "SELECT * FROM Users WHERE warnings >= 3;"
        return self.execute(SQL_COMMAND,  fetchall=True)

    def select_all_users(self):
        return self.execute("SELECT * FROM Users;", fetchall=True)

    def update_last_refresh_date(self, time, user_ids):
        SQL_COMMAND = "UPDATE Users SET lastRefreshDate=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(time, user_ids), commit=True)

    def update_user_transaction(self, transaction, user_ids):
        SQL_COMMAND = "UPDATE Users SET userTransaction=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(transaction, user_ids), commit=True)

    def update_user_wallet(self, TokenA, user_ids):
        SQL_COMMAND = "UPDATE Users SET userWallet=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(TokenA, user_ids), commit=True)

    def update_verification_wallet_address(self, TokenB, user_ids):
        SQL_COMMAND = "UPDATE Users SET verificationWalletAddress=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(TokenB, user_ids), commit=True)

    def update_verification_wallet_privet_hex(self, DollarAmount, user_ids):
        SQL_COMMAND = "UPDATE Users SET verificationWalletPrivetHex=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(DollarAmount, user_ids), commit=True)

    def update_warnings(self, warnings, user_ids):
        SQL_COMMAND = "UPDATE Users SET warnings=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(warnings, user_ids), commit=True)

    def update_verification_wallet_privet_seed(self, CrossExchange, user_ids):
        SQL_COMMAND = "UPDATE Users SET verificationWalletPrivetSeed=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(CrossExchange, user_ids), commit=True)

    def update_user(self, user_ids, time, TokenA, TokenB, DollarAmount):
        SQL_COMMAND = "UPDATE Users SET time=? , TokenA=? , TokenB=? , DollarAmount=?  WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(time, TokenA, TokenB, DollarAmount, user_ids), commit=True)

    def mak_admin(self, adminRights, user_ids):
        SQL_COMMAND = "UPDATE Users SET adminRights=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(adminRights, user_ids), commit=True)

    def update_verification_process(self, verificationProcess, user_ids):
        SQL_COMMAND = "UPDATE Users SET verificationProcess=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(verificationProcess, user_ids), commit=True)

    def update_username_and_fullname(self, username, name, user_ids):
        SQL_COMMAND = "UPDATE Users SET username=?, name=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(username, name, user_ids), commit=True)

    def delete_all_users(self):
        return self.execute("DELETE FROM Users WHERE True", commit=True)

    def delete_user(self, user_ids):
        SQL_COMMAND = "DELETE FROM Users WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(user_ids,), commit=True)

    @staticmethod
    def format_args(SQL_COMMAND, parameters: dict):

        SQL_COMMAND += " AND ".join([
            f" {item} =?" for item in parameters
        ])

        return SQL_COMMAND, tuple(parameters.values())


def logger(statement):
    print(f"""
------------------------------------
Executing:
{statement}
------------------------------------
""")
