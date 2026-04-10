import { FormEvent, useEffect, useMemo, useState } from "react";

type Side = "buy" | "sell";

type Trade = {
  id: string;
  symbol: string;
  side: Side;
  quantity: number;
  price: number;
  timestamp: string;
};

type DepthLevel = {
  price: number;
  size: number;
};

const SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"];

function buildSeries(seed = 67200) {
  return Array.from({ length: 64 }, (_, i) => {
    const trend = Math.sin(i / 6) * 370;
    const wave = Math.cos(i / 3) * 145;
    const drift = i * 4.5;
    return Number((seed + trend + wave + drift).toFixed(2));
  });
}

function toPolyline(values: number[]) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  return values
    .map((value, idx) => {
      const x = (idx / (values.length - 1)) * 100;
      const y = 100 - ((value - min) / range) * 100;
      return `${x},${y}`;
    })
    .join(" ");
}

function useDepth(midPrice: number) {
  return useMemo(() => {
    const bids: DepthLevel[] = Array.from({ length: 12 }, (_, i) => ({
      price: Number((midPrice - (i + 1) * 4.2).toFixed(2)),
      size: Number((Math.random() * 5 + 0.4).toFixed(3)),
    }));
    const asks: DepthLevel[] = Array.from({ length: 12 }, (_, i) => ({
      price: Number((midPrice + (i + 1) * 4.2).toFixed(2)),
      size: Number((Math.random() * 5 + 0.4).toFixed(3)),
    }));
    return { bids, asks };
  }, [midPrice]);
}

export function LiveDashboard() {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [side, setSide] = useState<Side>("buy");
  const [quantity, setQuantity] = useState(0.135);
  const [price, setPrice] = useState(67325.2);
  const [leverage, setLeverage] = useState(8);
  const [series, setSeries] = useState<number[]>(() => buildSeries());
  const [trades, setTrades] = useState<Trade[]>([]);
  const [message, setMessage] = useState("Route a ticket to simulate exchange matching.");

  const latest = series.at(-1) ?? price;
  const depth = useDepth(latest);
  const graph = useMemo(() => toPolyline(series), [series]);

  useEffect(() => {
    const timer = setInterval(() => {
      setSeries((previous) => {
        const last = previous.at(-1) ?? 67200;
        const step = (Math.random() - 0.48) * 110;
        const next = Number((last + step).toFixed(2));
        setPrice(next);
        return [...previous.slice(1), next];
      });
    }, 1200);

    return () => clearInterval(timer);
  }, []);

  const kpis = useMemo(() => {
    const open = series[0];
    const pct = (((latest - open) / open) * 100).toFixed(2);
    return {
      mark: latest.toFixed(2),
      spread: `${(Math.random() * 0.03 + 0.01).toFixed(3)}%`,
      volume: `${(Math.random() * 2200 + 8900).toFixed(0)} BTC`,
      change: pct,
      latency: `${(18 + Math.random() * 16).toFixed(1)} ms`,
      fillRate: `${(98.2 + Math.random() * 1.5).toFixed(2)}%`,
    };
  }, [latest, series]);

  const pulseMarket = () => {
    const step = (Math.random() - 0.48) * 140;
    const next = Number((latest + step).toFixed(2));
    setSeries((previous) => [...previous.slice(1), next]);
    setPrice(next);
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const order: Trade = {
      id: `MX-${Math.random().toString(36).slice(2, 9).toUpperCase()}`,
      symbol,
      side,
      quantity,
      price,
      timestamp: new Date().toLocaleTimeString(),
    };

    setTrades((previous) => [order, ...previous].slice(0, 14));
    setMessage(
      `${order.id} queued · ${order.side.toUpperCase()} ${order.quantity} ${order.symbol} @ ${order.price} (x${leverage})`
    );
    pulseMarket();
  };

  return (
    <div className="dashboard-shell">
      <header className="header">
        <div>
          <h1>MoXis Trader</h1>
          <p>Derivatives simulation terminal with real-time depth and strategy execution previews.</p>
        </div>
        <button className="pulse" onClick={pulseMarket} type="button">
          Simulate Tick
        </button>
      </header>

      <section className="grid">
        <article className="card kpi"><h4>Mark Price</h4><strong>${kpis.mark}</strong></article>
        <article className="card kpi"><h4>24h Change</h4><strong>{kpis.change}%</strong></article>
        <article className="card kpi"><h4>Spread</h4><strong>{kpis.spread}</strong></article>
        <article className="card kpi"><h4>P95 Latency</h4><strong>{kpis.latency}</strong></article>
        <article className="card kpi"><h4>24h Volume</h4><strong>{kpis.volume}</strong></article>
        <article className="card kpi"><h4>Fill Rate</h4><strong>{kpis.fillRate}</strong></article>

        <article className="card chart">
          <div className="chart-head">
            <h3>{symbol} Perpetual</h3>
            <div className="timeframe">1m · 5m · 15m · 1h</div>
          </div>
          <svg viewBox="0 0 100 100" preserveAspectRatio="none">
            <defs>
              <linearGradient id="curveFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#e9f66f" stopOpacity="0.45" />
                <stop offset="100%" stopColor="#e9f66f" stopOpacity="0.01" />
              </linearGradient>
            </defs>
            <polyline points={graph} />
            <polygon points={`0,100 ${graph} 100,100`} fill="url(#curveFill)" />
          </svg>
        </article>

        <article className="card orderbook">
          <h3>Order Book</h3>
          <div className="depth-grid">
            <div>
              <h5>Asks</h5>
              {depth.asks.map((ask) => (
                <div key={`a-${ask.price}`} className="depth-row sell">
                  <span>{ask.price.toFixed(2)}</span>
                  <span>{ask.size.toFixed(3)}</span>
                </div>
              ))}
            </div>
            <div>
              <h5>Bids</h5>
              {depth.bids.map((bid) => (
                <div key={`b-${bid.price}`} className="depth-row buy">
                  <span>{bid.price.toFixed(2)}</span>
                  <span>{bid.size.toFixed(3)}</span>
                </div>
              ))}
            </div>
          </div>
        </article>

        <article className="card execution">
          <h3>Place Order</h3>
          <form onSubmit={handleSubmit}>
            <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
              {SYMBOLS.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
            <select value={side} onChange={(e) => setSide(e.target.value as Side)}>
              <option value="buy">Market Buy</option>
              <option value="sell">Market Sell</option>
            </select>
            <input
              type="number"
              value={quantity}
              min={0.001}
              step={0.001}
              onChange={(e) => setQuantity(Number(e.target.value))}
            />
            <input type="number" value={price} step={0.1} onChange={(e) => setPrice(Number(e.target.value))} />
            <input
              type="range"
              min={1}
              max={30}
              value={leverage}
              onChange={(e) => setLeverage(Number(e.target.value))}
            />
            <button type="submit">Confirm</button>
          </form>
          <div className="leverage">Leverage: x{leverage}</div>
          <div className="result">{message}</div>
        </article>

        <article className="card tape">
          <h3>Trade Tape</h3>
          <div className="ticker">
            {trades.length === 0 ? (
              <div className="muted">No trades yet</div>
            ) : (
              trades.map((trade) => (
                <div className="tape-item" key={trade.id}>
                  <span>{trade.timestamp}</span>
                  <span>{trade.symbol}</span>
                  <span className={trade.side}>{trade.side.toUpperCase()}</span>
                  <span>{trade.quantity}</span>
                  <span>${trade.price}</span>
                </div>
              ))
            )}
          </div>
        </article>
      </section>

      <footer className="footer">
        <p>© 2022 Moses Achi.</p>
        <p>This is a simulation for demonstration purpose only.</p>
        <a href="https://github.com/mosesachizz/distributed-ai-trading-engine" target="_blank" rel="noreferrer">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 0C5.37 0 0 5.37 0 12a12 12 0 0 0 8.2 11.39c.6.11.82-.26.82-.58v-2.2c-3.34.73-4.04-1.42-4.04-1.42-.55-1.4-1.33-1.77-1.33-1.77-1.08-.74.08-.72.08-.72 1.2.08 1.82 1.22 1.82 1.22 1.05 1.8 2.76 1.28 3.43.98.1-.76.42-1.29.77-1.58-2.66-.3-5.47-1.34-5.47-5.94 0-1.3.47-2.35 1.23-3.18-.12-.3-.53-1.52.12-3.17 0 0 1-.32 3.3 1.22a11.5 11.5 0 0 1 6 0c2.29-1.54 3.28-1.22 3.28-1.22.65 1.65.24 2.87.12 3.17.77.83 1.23 1.88 1.23 3.18 0 4.62-2.82 5.64-5.51 5.94.44.37.83 1.09.83 2.2v3.26c0 .32.22.7.83.58A12 12 0 0 0 24 12c0-6.63-5.37-12-12-12Z" />
          </svg>
          View source code
        </a>
      </footer>
    </div>
  );
}
