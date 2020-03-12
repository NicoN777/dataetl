from framework.jobs.base import *

def ora_to_ora():
    return [DB('cb',
            'WOLF',
            'TURTLE',
            """SELECT EXTRACTION_DATE, CURRENCY, SELL_PRICE, 
            SPOT_PRICE, BUY_PRICE FROM CB_BTC_PRICE_HISTORY""",
            """INSERT INTO CB_BTC_PRICE_HISTORY(EXTRACTION_DATE,
            CURRENCY, SELL_PRICE, SPOT_PRICE, BUY_PRICE ) 
            VALUES(:EXTRACTION_DATE,:CURRENCY,:SELL_PRICE,
            :SPOT_PRICE,:BUY_PRICE )"""),
            DB('cmc',
             'WOLF',
             'TURTLE',
             """SELECT EXTRACTION_DATE, CIRCULATING_SUPPLY, 
                TOTAL_SUPPLY, MAX_SUPPLY, USD_PRICE, 
                VOLUME_24_HOURS, PERCENT_CHANGE_1, 
                PERCENT_CHANGE_24, PERCENT_CHANGE_7_DAYS, 
                MARKET_CAP, LAST_UPDATED FROM CMC_PRICE_HISTORY""",

             """INSERT INTO CMC_PRICE_HISTORY(
                EXTRACTION_DATE, CIRCULATING_SUPPLY, 
                TOTAL_SUPPLY, MAX_SUPPLY, USD_PRICE, 
                VOLUME_24_HOURS, PERCENT_CHANGE_1, 
                PERCENT_CHANGE_24, PERCENT_CHANGE_7_DAYS, 
                MARKET_CAP, LAST_UPDATED
                ) 
                VALUES(
                :EXTRACTION_DATE, :CIRCULATING_SUPPLY, 
                :TOTAL_SUPPLY, :MAX_SUPPLY, :USD_PRICE, 
                :VOLUME_24_HOURS, :PERCENT_CHANGE_1, 
                :PERCENT_CHANGE_24, :PERCENT_CHANGE_7_DAYS, 
                :MARKET_CAP, :LAST_UPDATED)""")]

def ora_to_bucket():
    return [Bucket('cb_bucket', 'WOLF', 'CAT', """SELECT * FROM CB_BTC_PRICE_HISTORY"""),
            Bucket('cmc_bucket', 'WOLF', 'CAT', """SELECT * FROM CMC_PRICE_HISTORY""")]

def ora_to_rmq():
    return [MessageQ('cb_rmq', 'WOLF', """SELECT * FROM CB_BTC_PRICE_HISTORY""", 'General', 'CB'),
            MessageQ('cb_rmq', 'WOLF', """SELECT * FROM CMC_PRICE_HISTORY""", 'General', 'CMC')]
