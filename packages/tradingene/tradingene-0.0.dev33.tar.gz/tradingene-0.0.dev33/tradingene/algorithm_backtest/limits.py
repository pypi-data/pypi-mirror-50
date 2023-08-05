from datetime import datetime

################################################################################
#                               SLIPPAGEs constants
################################################################################
BTCUSD_SLIPPAGE = 15
ETHUSD_SLIPPAGE = 3
LTCUSD_SLIPPAGE = 0.002
ETHBTC_SLIPPAGE = 0.000002
LTCBTC_SLIPPAGE = 0.0000002
DSHBTC_SLIPPAGE = 0.000002
XRPBTC_SLIPPAGE = 0.00000002
EOSUSD_SLIPPAGE = 0.0002
EOSBTC_SLIPPAGE = 0.00000002
XBTUSD_SLIPPAGE = 1
SI_SLIPPAGE = 2
RTS_SLIPPAGE = 10
BR_SLIPPAGE = 0.01
SBRF_SLIPPAGE = 2
GAZR_SLIPPAGE = 2
AAPL_SLIPPAGE = 0.02
BRNICE_SLIPPAGE = 0.02
MSNP500_SLIPPAGE = 0.5
NQ100_SLIPPAGE = 0.5
AMZN_SLIPPAGE = 0.02
GOOGL_SLIPPAGE = 0.02
BABA_SLIPPAGE = 0.02
NVDA_SLIPPAGE = 0.02
FB_SLIPPAGE = 0.01
NFLX_SLIPPAGE = 0.01

################################################################################

################################################################################
#                               Data constants
################################################################################
LOOKBACK_PERIOD = 150
################################################################################

################################################################################
#                               Backtest constants
################################################################################
EARLISET_START = datetime(2017, 1, 1)
MAX_AVAILABLE_VOLUME = 1

################################################################################
#                               Instrument's IDs
################################################################################
instrument_ids = {
    'btcusd': 18,
    'ethusd': 19,
    'ltcusd': 20,
    'ethbtc': 22,
    'ltcbtc': 23,
    'dshbtc': 24,
    'xrpbtc': 25,
    'eosusd': 26,
    'eosbtc': 27,
    'xbtusd': 28,
    'si': 42,
    'rts': 43,
    'br': 44,
    'sbrf': 45,
    'gazr': 46,
    'aapl': 50,
    'brnice': 51,
    'msnp500': 52,
    'nq100': 53,
    'amzn': 54,
    'googl': 55,
    'baba': 56,
    'nvda': 57,
    'fb': 58,
    'nflx': 59        
}

################################################################################
#                               MOEX Tickers
################################################################################
moex_tickers = [
    'si', 'rts', 'br', 'sbrf', 'gazr', 'aapl', 'brnice', 'msnp500', 'nq100', 'amzn', 'googl', 'baba', 'nvda', 'fb', 'nflx'
]