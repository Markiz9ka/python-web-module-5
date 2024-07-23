import aiohttp
import asyncio
import datetime
import sys

API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"

async def fetch_exchange_rate(session, date):
    try:
        async with session.get(API_URL.format(date=date)) as response:
            if response.status != 200:
                print(f"Error:{response.status}")
                return None
            data = await response.json()
            return data
    except Exception as e:
        print(f"Exception: {e}")
        return None

async def get_exchange_rates(days):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(days):
            date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%d.%m.%Y')
            tasks.append(fetch_exchange_rate(session, date))
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result:
                print(f"Date: {result['date']}")
                for rate in result.get('exchangeRate', []):
                    if rate.get('currency') in ['USD', 'EUR']:
                        print(f"  {rate['currency']}: Buy - {rate['purchaseRate']}, Sell - {rate['saleRate']}")

def validate_days(days):
    try:
        days = int(days)
        if days < 1 or days > 10:
            raise ValueError
        return days
    except ValueError:
        print("Please enter a valid number of days between 1 and 10.")

if __name__ == "__main__":
    
    days = validate_days(sys.argv[1])
    asyncio.run(get_exchange_rates(days))
