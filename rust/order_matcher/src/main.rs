use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Order {
    id: String,
    symbol: String,
    side: String,
    qty: f64,
    price: f64,
}

fn should_match(bid: &Order, ask: &Order) -> bool {
    bid.symbol == ask.symbol && bid.price >= ask.price && bid.side == "buy" && ask.side == "sell"
}

fn main() {
    let bid = Order {
        id: "bid-1".to_string(),
        symbol: "AAPL".to_string(),
        side: "buy".to_string(),
        qty: 10.0,
        price: 195.0,
    };
    let ask = Order {
        id: "ask-1".to_string(),
        symbol: "AAPL".to_string(),
        side: "sell".to_string(),
        qty: 10.0,
        price: 194.5,
    };

    println!("{}", should_match(&bid, &ask));
}
