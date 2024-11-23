# visualizer.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from config import CHART_FILE

class PriceVisualizer:
    def __init__(self):
        plt.style.use('dark_background')
        self.fig_size = (20, 12)
        
    def create_price_chart(self, df):
        """Creates a comprehensive price chart with multiple subplots"""
        # Create figure and grid
        fig = plt.figure(figsize=self.fig_size)
        gs = fig.add_gridspec(3, 1, height_ratios=[3, 1, 1], hspace=0.3)
        
        # Main price plot
        ax1 = fig.add_subplot(gs[0])
        self._plot_prices(df, ax1)
        
        # Volume subplot
        ax2 = fig.add_subplot(gs[1])
        self._plot_volume(df, ax2)
        
        # Price distribution subplot
        ax3 = fig.add_subplot(gs[2])
        self._plot_price_distribution(df, ax3)
        
        self._add_finishing_touches(fig)
        return fig

    def _plot_prices(self, df, ax):
        """Plot main price chart with moving averages"""
        # Plot high and low prices
        ax.plot(df.index, df['avgHighPrice'], 
                color='#00ff00', label='High Price', alpha=0.8)
        ax.plot(df.index, df['avgLowPrice'], 
                color='#ff3333', label='Low Price', alpha=0.8)
        
        # Add moving averages
        self._add_moving_averages(df, ax)
        
        # Formatting
        ax.set_title('Price History with Moving Averages', pad=20)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.2)
        ax.set_ylabel('Price (gp)')

    def _add_moving_averages(self, df, ax):
        """Add different moving averages to the price chart"""
        # 1-hour MA (12 5-minute periods)
        ma_1h = df['avgHighPrice'].rolling(window=12).mean()
        ax.plot(df.index, ma_1h, 
                color='yellow', label='1h MA', alpha=0.6)
        
        # 4-hour MA (48 5-minute periods)
        ma_4h = df['avgHighPrice'].rolling(window=48).mean()
        ax.plot(df.index, ma_4h, 
                color='cyan', label='4h MA', alpha=0.6)
        
        # 24-hour MA (288 5-minute periods)
        ma_24h = df['avgHighPrice'].rolling(window=288).mean()
        ax.plot(df.index, ma_24h, 
                color='magenta', label='24h MA', alpha=0.6)

    def _plot_volume(self, df, ax):
        """Create volume subplot"""
        # Combine high and low volumes
        total_volume = df['highPriceVolume'] + df['lowPriceVolume']
        
        # Plot volume bars
        ax.bar(df.index, total_volume, 
               color='#304C89', alpha=0.7, width=0.001)
        
        # Calculate and plot moving average of volume
        volume_ma = total_volume.rolling(window=288).mean()  # 24h MA
        ax.plot(df.index, volume_ma, 
                color='#FF9800', label='Volume MA (24h)', alpha=0.8)
        
        ax.set_title('Trading Volume')
        ax.set_ylabel('Volume')
        ax.grid(True, alpha=0.2)
        ax.legend()

    def _plot_price_distribution(self, df, ax):
        """Create price distribution histogram"""
        prices = df['avgHighPrice'].dropna()
        ax.hist(prices, bins=50, color='#304C89', alpha=0.7)
        ax.axvline(prices.mean(), color='#FF9800', 
                   linestyle='dashed', linewidth=2, label='Mean Price')
        ax.axvline(prices.median(), color='#00ff00', 
                   linestyle='dashed', linewidth=2, label='Median Price')
        
        ax.set_title('Price Distribution')
        ax.set_xlabel('Price (gp)')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.2)
        ax.legend()

    def _add_finishing_touches(self, fig):
        """Add final formatting to the figure"""
        # Add title
        fig.suptitle('Blood Rune Market Analysis', 
                    fontsize=16, y=0.95)
        
        # Add timestamp
        plt.figtext(0.99, 0.01, f'Generated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}', 
                   ha='right', va='bottom', fontsize=8)

    def save_plot(self, filename=CHART_FILE):
        """Save the current figure"""
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

    def show_plot(self):
        """Display the current figure"""
        plt.show()