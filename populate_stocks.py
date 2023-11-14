import config
import alpaca_trade_api as tradeapi
import psycopg2 
import psycopg2.extras
connection = psycopg2.connect(host=config.DB_HOST,database=config.DB_NAME,user=config.DB_USER, password= config.DB_PASS) 
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

api = tradeapi.REST(config.API_KEY,config.SECRET_KEY,base_url=config.BASE_URL)

assets = api.list_assets()


for asset in assets:
    print(f"Inserting a stock {asset.name},{asset.symbol}")
    cursor.execute("""
        insert into stock (name,symbol,exchange, is_etf) values (%s,%s,%s,%s)
    """,(asset.name,asset.symbol,asset.exchange, False))


connection.commit()
