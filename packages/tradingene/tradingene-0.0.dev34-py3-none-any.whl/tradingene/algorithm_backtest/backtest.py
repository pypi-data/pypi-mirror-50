import sys
import time
from datetime import datetime, timedelta
from warnings import warn
import numpy as np
from tradingene.algorithm_backtest.environment import Environment
from tradingene.algorithm_backtest.position import Position
from tradingene.algorithm_backtest.time_event import TimeEvent
from tradingene.algorithm_backtest.price_event import PriceEvent
import tradingene.algorithm_backtest.limits as limits
from tradingene.data.data import Data, dt
from tradingene.data.date_init import date_init

#from tradingene.ind.slippage_estimation_corwin_schultz import corwin_schultz


class Backtest(Environment):
    """ Runs the backtest.

        Constructor of this class will automatically 
        invoke by the inherited class TradeActivity.

        Arguments:
            args (tuple): Tuple of variables that needed for initialization
                of the super class Algorithm.

        Attributes:
            history_data (dict): Contains loaded history data 
                of the specified instrument.
            completed_timeframes (list): List of timeframes that was completed
                while run of backtest.
            completed_tickers (list): List of tickers that have at least one
                completed timeframe and appears in the last minute candle that
                was send to backtest.
            now (int): Time of the beggining of the most recent minute candle.
            recent_price (tuple): The most recent price of an instrument.
                Minute candle divides into four ticks:
                a) if a candle goes down: open, high, low, close;
                b) otherwise: open, low, high, close.
            slippage (float): slippage. Specified for each instrument.
            instruments (set): Set of intances of Instrument class.
                each instance contains information about opens, highs,
                lows, closes, volumes, values of indicators. 
            time_events (list): List of instances of TimeEvents class.
                Time events added by user in the onBar function.
            price_events (list): List of instances of PriceEvent class.
                Price events added by user in the onBar function.
    """

    def __init__(self, *args):
        name, regime = args[0], args[1]
        start_date, end_date = args[2], args[3]
        super(Backtest, self).__init__(name, regime, start_date, end_date)
        self.history_data = dict()
        self.completed_timeframes = list()
        self.completed_tickers = list()
        self._now = 0
        self._recent_price = (0, 0)
        self.slippage = 0
        self._sl_or_tp = False
        self._data_initialized = False
        self._on_bar_params = None


################################################################################

    def run_backtest(self, on_bar_function, *args, shift=0, show_progress=True, **kargs):
        """ Runs backtest of an algorithm. 
        
        Args:
            on_bar_function (function): user-define function
                that is called after each fully formed candle.
            shift (int): 

        Returns:
            None.
        
        Raises:
            TypeError: if on_bar_function is not callable.
            RuntimeError: if ticker_timeframe is empty, i.e.
                no instrument was added.
        
        """
        
        if not callable(on_bar_function):
            err_str = "on_bar_function must be callable, not of "+\
                      "{} type!".format(type(on_bar_function).__name__)
            raise TypeError(err_str)
        if not self.ticker_timeframes:
            raise RuntimeError("No instrument was added!")
        code_methods = on_bar_function.__code__.co_names
        if any(elem in code_methods for elem in ('setSL', 'setTP', 'setSLTP')):
            self._sl_or_tp = True
        if not self._data_initialized:
            sys.stdout.write("Loading data!\n")
            sys.stdout.flush()
            
            ###############################################################
            #           Only for one instrument
            ###############################################################
            self.pre_start_date, self.start_date, self.end_date = date_init(self)
            self._load_data(self.start_date, self.end_date, shift)
            sys.stdout.write("Data loaded!\n")
            self._set_slippage()
            self._data_initialized = True
        else:
            self._reinitialize_data()
        self._set_parameters_for_onbar(on_bar_function, args = args, kargs = kargs)
        self._initialize_candles()
        candle_generator = self._iterate_data(self.pre_start_date, self.end_date)
        self._run_generator(candle_generator, on_bar_function, show_progress, shift)


    def _run_generator(self,
                       generator,
                       on_bar_function,
                       show_progress,
                       shift=0
                       ):
        candles = next(generator)
        minutes_left = -shift + 1
        self._update_instruments(candles)
        try:
            complete_timeframes = list()
            complete_tickers = list()
            instrs = set()
            while True:
                candles = next(generator)
                self._update_recent_price(candles)
                time_frames = self._list_all_timeframes()
                complete_timeframes = \
                        self._completed_timeframes(minutes_left, time_frames)
                complete_tickers = self._completed_tickers(
                    complete_timeframes, complete_tickers)
                on_bar_tickers = {ticker \
                        for ticker in complete_tickers if ticker in candles}
                instrs |= self._completed_instruments(complete_tickers,
                                                      complete_timeframes)
                call = {
                    instrument
                    for instrument in instrs
                    if instrument.ticker in on_bar_tickers
                }
                for instr in call:
                    instr = self._reload_instrument(
                        instr, candles, show_bar=show_progress)
                instrs -= call
                complete_tickers = list(set(complete_tickers) - on_bar_tickers)
                if self.start_date_int < self._now:
                    [on_bar_function(onbar_call, *self._on_bar_params) for onbar_call in call]
                minutes_left += 1
                self._update_instruments(candles)
                if self._sl_or_tp:
                    self._minute_to_ticks(candles)
        except StopIteration:
            sys.stdout.write("\n")
            sys.stdout.flush()
            instr_list = [instr for instr in self.instruments]
            list(map(self._update_last_candle, instr_list))


    def _set_parameters_for_onbar(self, on_bar_function, **params):
        number_of_arguments = on_bar_function.__code__.co_argcount
        on_bar_args = on_bar_function.__code__.co_varnames[1:number_of_arguments]
        total_len = 0
        for value in params['kargs'].values():
            if not isinstance(value, (str, int, float, complex)):
                raise TypeError("Parameter should be str, int, float or complex!")
            else:
                total_len += 1
        if total_len != number_of_arguments - 1:
            err_str = "Number of variables that were sent greater than "\
                        + "number of arguments of {}".format(on_bar_function.__name__)
            raise RuntimeError(err_str) 
        if set(on_bar_args) == set(params['kargs'].keys()):
            self._on_bar_params = tuple(params['kargs'][key] for key in on_bar_args)
        else:
            raise NameError("Names of variables in run_backtest and onBar do not coincide!")
     

    def _update_recent_price(self, candles):
        ticker = list(self.ticker_timeframes)[0]
        if ticker in candles.keys():
            self.recent_price = (candles[ticker].open, 1)


    def _minute_to_ticks(self, candles):
        ticker = list(self.ticker_timeframes)[0]
        if ticker in candles.keys():
            self.recent_price = (candles[ticker].open, 1)
            if candles[ticker].open < candles[ticker].close:
                self.recent_price = (candles[ticker].low, 1)
            else:
                self.recent_price = (candles[ticker].high, 1)
            if candles[ticker].open < candles[ticker].close:
                self.recent_price = (candles[ticker].high, 1)
            else:
                self.recent_price = (candles[ticker].low, 1)
            self.recent_price = (candles[ticker].close, 1)


    def _iterate_data(self, start_date, end_date):
        current_time = start_date
        backtest_time = int(current_time.strftime("%Y%m%d%H%M%S"))
        time_ticks = dict.fromkeys(self.ticker_timeframes, -1)
        while current_time <= end_date:
            self.now = backtest_time
            ans = dict()
            for ticker in self.ticker_timeframes:
                ind = time_ticks[ticker]
                try:
                    ticker_time = self.history_data[ticker]['time'].iloc[ind]
                except:
                    continue
                if ticker_time == backtest_time:
                    time_ticks[ticker] -= 1
                    ans[ticker] = self.history_data[ticker].iloc[ind]
                else:
                    pass
            current_time = current_time + timedelta(minutes=1)
            backtest_time = int(current_time.strftime("%Y%m%d%H%M%S"))
            yield ans


    def _update_instruments(self, candles):
        for instrument in self.instruments:
            ticker = instrument.ticker
            if instrument.time[0] == 0:
                instrument.time[0] = self.now
            if ticker in candles.keys():
                candle = candles[ticker]
            else:
                continue
            if instrument.open[0] == 0:
                instrument.open[0] = candle.open
            instrument.high[0] = max(instrument.high[0], candle['high'])
            if instrument.low[0] == 0:
                instrument.low[0] = candle['low']
            else:
                instrument.low[0] = min(instrument.low[0], candle['low'])
            instrument.close[0] = candle['close']
            instrument.vol[0] += candle['vol']


    def _reload_instrument(self, instrument, candles, show_bar):
        def correct_candle_time(time_, timeframe):
            minutes_ = ((time_ // 100) % 100)
            hours_ = ((time_ // 10000) % 100)
            days_ = ((time_ // 1000000) % 100)
            total_minutes = (days_ - 1) * 1440 + hours_ * 60 + minutes_
            total_minutes %= timeframe
            minutes_ = (time_) % timeframe
            time_ = datetime(*(time.strptime(str(time_), \
                                            "%Y%m%d%H%M%S")[0:6]))
            time_ -= timedelta(minutes=total_minutes)
            time_ = int(time_.strftime("%Y%m%d%H%M%S"))
            return time_

        if show_bar:
            self._update_progress_bar()
        candle = candles[instrument.ticker]
        for instr in self.instruments:
            if instr.ticker == instrument.ticker and \
               instr.timeframe == instrument.timeframe:
                time_ = datetime(*(time.strptime(str(self.now), \
                                           "%Y%m%d%H%M%S")[0:6]))
                begin_time = datetime(*time.strptime(str(instr.time[0]), \
                                            "%Y%m%d%H%M%S")[0:6])
                elapsed = (time_ - begin_time).seconds // 60
                open_price = np.array([candle['open']])

                last_time = instr.time[0]
                time_ -= timedelta(minutes=elapsed % instr.timeframe)
                new_time = int(time_.strftime("%Y%m%d%H%M%S"))
                instr.time = np.concatenate(([new_time], instr.time[:-1]))
                instr.open = np.concatenate((open_price, instr.open[:-1]))
                instr.high = np.concatenate((open_price, instr.high[:-1]))
                instr.low = np.concatenate((open_price, instr.low[:-1]))
                instr.close = np.concatenate((open_price, instr.close[:-1]))
                instr.vol = np.concatenate(([0], instr.vol[:-1]))
                last_candle = np.array([(last_time, instr.open[1], \
                                        instr.high[1], instr.low[1], \
                                        instr.close[1], instr.vol[1])], \
                                        dtype = dt)
                new_candle = np.array([(new_time, instr.open[0], instr.high[0],\
                                        instr.low[0], instr.close[0], \
                                        instr.vol[0])], dtype = dt)
                instr.rates[0] = last_candle[0]
                instr.rates = np.concatenate((new_candle, instr.rates[:-1]))
                instr.candle_start_time = new_time
                if instr.candles is not None:
                    instr.candles[instr.candle_ind] = last_candle
                    instr.candles[instr.candle_ind + 1] = new_candle
                    instr.candle_ind += 1
        return instrument


    def _update_last_candle(self, instr):
        open_price = np.array([0.])
        time_ = datetime(*(time.strptime(str(instr.time[0]), \
                                    "%Y%m%d%H%M%S")[0:6]))
        if time_ + timedelta(minutes=instr.timeframe) > self.end_date:
            end_time = self.end_date
        else:
            end_time = time_ + timedelta(minutes=instr.timeframe)
        end_time = int(end_time.strftime("%Y%m%d%H%M%S"))
        instr.time = np.concatenate(([end_time], instr.time[:-1]))
        instr.open = np.concatenate((open_price, instr.open[:-1]))
        instr.high = np.concatenate((open_price, instr.high[:-1]))
        instr.low = np.concatenate((open_price, instr.low[:-1]))
        instr.close = np.concatenate((open_price, instr.close[:-1]))
        instr.vol = np.concatenate(([0], instr.vol[:-1]))
        last_candle = np.array([(instr.time[1], instr.open[1], \
                                instr.high[1], instr.low[1], \
                                instr.close[1], instr.vol[1])], \
                                dtype = dt)
        new_candle = np.array([(end_time, instr.open[0], \
                                instr.high[0], instr.low[0],\
                                instr.close[0], instr.vol[0])],\
                                dtype = dt)
        instr.candles[instr.candle_ind] = last_candle
        instr.candles[instr.candle_ind+1] = new_candle
        instr.rates[0] = last_candle[0]
        instr.rates = np.concatenate((new_candle, instr.rates[:-1]))
        if instr.ticker in limits.moex_tickers:
            instr.time[0] = int(self.start_date.strftime("%Y%m%d%H%M%S"))
        last_ind = instr.candles.shape[0]
        first_ind = 50
        pre_end_date = self.end_date - timedelta(minutes=instr.timeframe)
        pre_end_date_int = int(pre_end_date.strftime("%Y%m%d%H%M%S"))
        for i in range(instr.candles.shape[0]-1, first_ind, -1):
            if instr.candles[i][0] != 0:
                last_ind = i
                break
        for i in range(last_ind):
            if instr.candles[i][0] == self.start_date_int:
                first_ind = i
                break
        instr.candles = instr.candles[first_ind:last_ind][::-1]


    def _completed_instruments(self, tickers, timeframes):
        instr = set()
        for instrument in self.instruments:
            ticker = instrument.ticker
            timeframe = instrument.timeframe
            if ticker in tickers and timeframe in timeframes:
                instr |= {instrument}
        return instr


    def _list_all_timeframes(self):
        time_frames = set()
        for value in self.ticker_timeframes.values():
            time_frames |= set(value)
        return sorted(list(time_frames))


    def _completed_timeframes(self, minutes_left, timeframes):
        completed_tfs = [timeframe\
                for timeframe in timeframes if minutes_left % timeframe == 0]
        return sorted(completed_tfs)


    def _completed_tickers(self, completed_timeframes, ct):
        ticker_set = {ticker for ticker, timeframes \
                          in self.ticker_timeframes.items()\
                          if set(completed_timeframes) & set(timeframes)}
        return list(ticker_set | set(ct))


    def _load_data(self, start_date, end_date, shift):
        for ticker in self.ticker_timeframes.keys():
            ticker_data = Data.load_data(ticker, self.pre_start_date, end_date)
            if shift:
                self.history_data[ticker] = ticker_data[:-shift]
            else:
                self.history_data[ticker] = ticker_data
            ticker_instrs = [
                instr for instr in self.instruments if instr.ticker == ticker
            ]
            for instr in ticker_instrs:
                instr.candle_start_time = int(
                    start_date.strftime("%Y%m%d%H%M%S"))


    def _update_progress_bar(self):
        start_date = self.start_date
        end_date = self.end_date
        current_time = datetime(*(time.strptime(str(self.now), \
                                            "%Y%m%d%H%M%S")[0:6]))
        if current_time < start_date:
            return
        progress = int(
            1000 * (1 - (end_date - current_time) / (end_date - start_date)))
        string = "\rBacktest in progress:\t"+\
                "[{0}{1}] {2}%".format('#'*(progress//20),'-'*(50-(progress//20)),progress/10)
        sys.stdout.write(string)
        sys.stdout.flush()


    def _initialize_candles(self):
        train_mins = self._calculate_number_of_minutes()
        for instr in self.instruments:
            number_of_bars = train_mins // instr.timeframe + 2
            instr.candles = np.zeros(number_of_bars, dtype=dt)
            instr.candle_ind = 0


    def _calculate_number_of_minutes(self):
        train_td = self.end_date - self.start_date
        train_minutes = 1440 * train_td.days + train_td.seconds // 60
        pre_td = self.start_date - self.pre_start_date
        pre_minutes = 1440 * pre_td.days + pre_td.seconds // 60
        return train_minutes+pre_minutes


    def _reinitialize_data(self):
        self.positions = list()
        self.time_events = list()
        self.price_events = list()


################################################################################
#       Set slippage
################################################################################

    def _set_slippage(self):
        ticker = list(self.ticker_timeframes)[0]
        if ticker == "btcusd":
            self.slippage = limits.BTCUSD_SLIPPAGE
        elif ticker == "ethusd":
            self.slippage = limits.ETHUSD_SLIPPAGE
        elif ticker == "ltcusd":
            self.slippage = limits.LTCUSD_SLIPPAGE
        elif ticker == "ethbtc":
            self.slippage = limits.ETHBTC_SLIPPAGE
        elif ticker == "ltcbtc":
            self.slippage = limits.LTCBTC_SLIPPAGE
        elif ticker == "dshbtc":
            self.slippage = limits.DSHBTC_SLIPPAGE
        elif ticker == "xrpbtc":
            self.slippage = limits.XRPBTC_SLIPPAGE
        elif ticker == "eosusd":
            self.slippage = limits.EOSUSD_SLIPPAGE
        elif ticker == "eosbtc":
            self.slippage = limits.EOSBTC_SLIPPAGE
        elif ticker == "xbtusd":
            self.slippage = limits.XBTUSD_SLIPPAGE
        elif ticker == "ethusd":
            self.slippage = limits.ETHUSD_SLIPPAGE
        elif ticker == "si":
            self.slippage = limits.SI_SLIPPAGE
        elif ticker == "rts":
            self.slippage = limits.RTS_SLIPPAGE
        elif ticker == "br":
            self.slippage = limits.BR_SLIPPAGE
        elif ticker == "sbrf":
            self.slippage = limits.SBRF_SLIPPAGE
        elif ticker == "gazr":
            self.slippage = limits.GAZR_SLIPPAGE
        elif ticker == "aapl":
            self.slippage = limits.AAPL_SLIPPAGE
        elif ticker == "brnice":
            self.slippage = limits.BRNICE_SLIPPAGE
        elif ticker == "msnp500":
            self.slippage = limits.MSNP500_SLIPPAGE
        elif ticker == "nq100":
            self.slippage = limits.NQ100_SLIPPAGE
        elif ticker == "amzn":
            self.slippage = limits.AMZN_SLIPPAGE
        elif ticker == "googl":
            self.slippage = limits.GOOGL_SLIPPAGE
        elif ticker == "baba":
            self.slippage = limits.BABA_SLIPPAGE
        elif ticker == "nvda":
            self.slippage = limits.NVDA_SLIPPAGE
        elif ticker == "fb":
            self.slippage = limits.FB_SLIPPAGE
        elif ticker == "nflx":
            self.slippage = limits.NFLX_SLIPPAGE
        else:
            self.slippage = 0.0
            #raise NameError("Slippage cannot be set, unknown ticker!")            


################################################################################

    @property
    def now(self):
        return self._now

    @now.setter
    def now(self, value):
        self._now = value
        TimeEvent.check(self)

    @now.deleter
    def now(self):
        self._now = None

    @property
    def recent_price(self):
        return self._recent_price

    @recent_price.setter
    def recent_price(self, value):
        self._recent_price = value[0]
        if value[1]:
            Position.check_sltp(self)
            PriceEvent.check(self)

    @recent_price.deleter
    def recent_price(self):
        self._recent_price = (None, 0)