import requests

# Lista de criptos suportadas (CoinGecko IDs)
crypto_list = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "LTC": "litecoin",
    "DOGE": "dogecoin"
}

def get_fiat_rate(base_currency, target_currency, amount):
    """Convert fiat currencies using exchangerate.host"""
    url = f"https://api.exchangerate.host/convert?from={base_currency}&to={target_currency}&amount={amount}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("success"):
            return data["result"], data["info"]["rate"]
        else:
            return None, None
    except requests.RequestException as e:
        print(f"❌ Error fetching fiat data for {target_currency}: {e}")
        return None, None

def get_crypto_rate(crypto_id, vs_currency, amount):
    """Convert cryptocurrency using CoinGecko"""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={vs_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        if crypto_id in data and vs_currency in data[crypto_id]:
            price = data[crypto_id][vs_currency]
            converted = amount / price
            return converted, price
        else:
            return None, None
    except requests.RequestException as e:
        print(f"❌ Error fetching crypto data for {crypto_id}: {e}")
        return None, None

def main():
    print("💱 Currency & Crypto Converter (Real-Time)")

    # Moeda base
    base = input("Enter base currency (e.g., USD, EUR, BRL): ").upper()

    # Moedas destino
    targets_input = input("Enter target currencies or cryptos separated by commas (e.g., BRL,USD,BTC,ETH): ")
    targets = [t.strip().upper() for t in targets_input.split(",")]

    # Valor a converter
    try:
        amount = float(input(f"Enter amount in {base}: "))
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return

    print("\n📊 Conversion results:")

    for target in targets:
        if target in crypto_list:
            converted, price = get_crypto_rate(crypto_list[target], base.lower(), amount)
            if converted is not None:
                print(f"{amount} {base} = {converted:.6f} {target} (1 {target} = {price:.2f} {base})")
            else:
                print(f"❌ Could not convert {base} to {target}")
        else:
            converted, rate = get_fiat_rate(base, target, amount)
            if converted is not None:
                print(f"{amount} {base} = {converted:.2f} {target} (Rate: {rate:.4f})")
            else:
                print(f"❌ Could not convert {base} to {target}")

if __name__ == "__main__":
    main()
