# AI Trader – Modular AI-Powered Trading System

**AI Trader** is my  project to build a clean, modular automated trading bot in Python.  
It follows a layered architecture (data ingestion → signal generation → risk management → execution → feedback) inspired by real quant trading systems.

Right now it's a strong **skeleton** with full structure, logging, configuration, and dry-run safety — ready to add real strategies, historical data replay, and eventually paper trading.

**Status (Feb 2026):** Simulation mode works (fake data or CSV replay coming soon). First simple strategy (e.g. SMA crossover) in progress.

## Why I built this

I want to learn algorithmic/quantitative trading from the ground up.  
Most beginner bots are messy one-file scripts — I decided to design it like a real system would work: modular, testable, configurable, and safe (no accidental live trades!).

Goals:
- Understand end-to-end trading pipeline
- Combine technical indicators, rules, news sentiment (future), and maybe ML
- Practice good software engineering in finance context
- Create something impressive for college apps / future quant roles

## Features (current & planned)

**Implemented / Working:**
- Layered architecture (data, signals, fusion, risk, execution, monitoring)
- Configurable via `config.yaml` (mode, symbols, risk %, timeframe…)
- Proper logging to console + file
- Dry-run / simulation mode (no real money at risk)
- Graceful error handling + shutdown
- Easy to extend with new strategies or data sources

**Coming soon / Roadmap:**
- Historical data replay (CSV from Binance/Yahoo)
- First real strategy: SMA crossover + basic rules
- Performance tracking (PnL, win rate, drawdown plot)
- Paper trading integration (e.g. Alpaca paper account or Binance testnet)
- Technical indicators module (Moving Averages, RSI…)
- Basic risk management (position sizing, stop-loss levels)
- Maybe simple ML pattern detection later

- real time Data Visualization 
## Project Structure
