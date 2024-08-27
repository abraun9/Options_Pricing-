from datetime import datetime, timedelta
from pricing_models import black_scholes, binomial_option_pricing, monte_carlo_option_pricing
from data_utils import get_stock_price, get_time_to_maturity, get_risk_free_rate, get_volatility

def get_valid_date():
    while True:
        date_str = input("Enter the expiration date (YYYY-MM-DD): ")
        try:
            expiration_date = datetime.strptime(date_str, "%Y-%m-%d")
            if expiration_date > datetime.now():
                return expiration_date
            else:
                print("Error: Expiration date must be in the future. Please try again.")
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")

def get_valid_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid number.")

def main():
    """
    Main function to execute the option pricing models and display results.
    """
    while True:
        ticker = input("Enter the stock symbol (e.g., AAPL): ").upper()
        S = get_stock_price(ticker)
        if S is not None:
            break
        print("Invalid stock ticker. Please try again.")

    K = get_valid_float("Enter the strike price of the option: ")
    expiration_date = get_valid_date()

    # Get input data
    T = get_time_to_maturity(expiration_date)
    r = get_risk_free_rate()

    # Calculate the date range for volatility
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Format dates as strings for the get_volatility function
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Get the volatility
    sigma = get_volatility(ticker, start_date_str, end_date_str)

    # Calculate option prices
    print("Calculating option prices...")
    call_price_bs = black_scholes(S, K, T, r, sigma, option_type='call')
    put_price_bs = black_scholes(S, K, T, r, sigma, option_type='put')
    call_price_binomial = binomial_option_pricing(S, K, T, r, sigma, 100, option_type='call')
    put_price_binomial = binomial_option_pricing(S, K, T, r, sigma, 100, option_type='put')
    call_price_mc = monte_carlo_option_pricing(S, K, T, r, sigma, simulations=10000, option_type='call')
    put_price_mc = monte_carlo_option_pricing(S, K, T, r, sigma, simulations=10000, option_type='put')

    # Print results
    print(f"Black-Scholes Call Price: {call_price_bs:.2f}")
    print(f"Black-Scholes Put Price: {put_price_bs:.2f}")
    print(f"Binomial Call Price: {call_price_binomial:.2f}")
    print(f"Binomial Put Price: {put_price_binomial:.2f}")
    print(f"Monte Carlo Call Price: {call_price_mc:.2f}")
    print(f"Monte Carlo Put Price: {put_price_mc:.2f}")

if __name__ == "__main__":
    main()