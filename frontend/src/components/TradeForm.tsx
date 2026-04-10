import { useState } from "react";
import { executeTrade, TradeRequest } from "../services/api";

const initial: TradeRequest = { symbol: "AAPL", side: "buy", quantity: 10, price: 200 };

export function TradeForm() {
  const [form, setForm] = useState<TradeRequest>(initial);
  const [result, setResult] = useState<string>("");

  const submit = async () => {
    const token = localStorage.getItem("token") || "";
    const response = await executeTrade(form, token);
    setResult(`Order ${response.order_id} accepted=${response.accepted}`);
  };

  return (
    <section>
      <h2>Execution Console</h2>
      <button onClick={submit}>Execute Trade</button>
      <pre>{result}</pre>
    </section>
  );
}
