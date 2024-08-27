import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    try:
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == 'put':
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
    except Exception as e:
        print(f"Error in Black-Scholes calculation: {e}")
        return None

def binomial_option_pricing(S, K, T, r, sigma, N, option_type='call'):
    try:
        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        q = (np.exp(r * dt) - d) / (u - d)
        
        asset_prices = np.zeros(N + 1)
        asset_prices[0] = S * d ** N
        
        for i in range(1, N + 1):
            asset_prices[i] = asset_prices[i - 1] * u / d
        
        option_values = np.maximum(0, (asset_prices - K) if option_type == 'call' else (K - asset_prices))
        
        for j in range(N - 1, -1, -1):
            for i in range(j + 1):
                option_values[i] = np.exp(-r * dt) * (q * option_values[i + 1] + (1 - q) * option_values[i])
        
        return option_values[0]
    except Exception as e:
        print(f"Error in Binomial option pricing calculation: {e}")
        return None

def monte_carlo_option_pricing(S, K, T, r, sigma, simulations=10000, option_type='call'):
    try:
        dt = T
        discount_factor = np.exp(-r * T)
        stock_price_end = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(dt) * np.random.randn(simulations))
        
        if option_type == 'call':
            option_payoff = np.maximum(0, stock_price_end - K)
        elif option_type == 'put':
            option_payoff = np.maximum(0, K - stock_price_end)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        
        return discount_factor * np.mean(option_payoff)
    except Exception as e:
        print(f"Error in Monte Carlo option pricing calculation: {e}")
        return None
