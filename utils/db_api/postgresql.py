from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
 
    def __init__(self):
        self.pool: Union[Pool, None] = None
        
    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        ) 

    async def execute(self, command, *args,
                    fetch: bool = False,
                    fetchval: bool = False,
                    fetchrow: bool = False,
                    execute: bool = False
                    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)    
            return result


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = ${num}' for num, item in enumerate(parameters.keys(),start=1)
        ])
        return sql, tuple(parameters.values())

    # 
    # 
    #       MENU TABLE
    # 
    # 

    #Create table menu SQL
    async def create_table_menu(self):
        sql = """
        CREATE TABLE IF NOT EXISTS MENU (
        id SERIAL PRIMARY KEY,
        picture BYTEA,
        product_name VARCHAR(50) NOT NULL,
        description VARCHAR(255) NULL,
        price FLOAT NOT NULL
        );
        """
        await self.execute(sql, execute=True)


    #
    async def add_menu_item(self, picture, product_name, description, price):
        sql = "INSERT INTO MENU (picture, product_name, description, price) VALUES ($1, $2, $3, $4) returning *"
        return await self.execute(sql, picture, product_name, description, price, fetchrow=True)


    async def select_menu_item(self, **kwargs):
        sql = "SELECT * FROM MENU WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    

    async def select_all_menu_items(self):
        sql = "SELECT * FROM MENU"
        return await self.execute(sql, fetch=True)




    # 
    # 
    #       USER TABLE
    # 
    # 


    #id - PK - telegeram_id
    #
    #is_bot


    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS USERS (
        id BIGINT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        username VARCHAR(255),
        language_code VARCHAR(5),
        is_premium BOOl,
        is_bot BOOL,
        supports_inline_queries BOOL
        );
        """

        await self.execute(sql, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM USERS"
        return await self.execute(sql, fetch=True)


    async def select_user(self, **kwargs):
        sql = "SELECT * FROM USERS WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    

    async def count_user(self):
        sql = "SELECT COUNT(*) FROM USERS"
        return await self.execute(sql, fetchval=True)

    async def add_user(self, id, first_name, last_name, username, language_code, is_premium, is_bot, supports_inline_queries):
        sql = "INSERT INTO USERS (id, first_name, last_name, username, language_code, is_premium, is_bot, supports_inline_queries) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) returning *"
        return await self.execute(sql, id, first_name, last_name, username, language_code, is_premium, is_bot, supports_inline_queries, fetchrow=True) 
      