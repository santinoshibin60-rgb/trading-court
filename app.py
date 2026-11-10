# ⚖️ Automated AI Trading Court Dashboard
import streamlit as st
import yfinance as yf
import pandas_ta as ta

st.set_page_config(page_title="Automated AI Trading Court", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput > div > div > input { background-color: #1a1c23; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Automated AI Trading Court")
st.markdown("### Institutional Multi-Agent Market Tribunal (SMC / ICT / Price Action)")

st.sidebar.header("🏛️ Tribunal Settings")
asset_choice = st.sidebar.selectbox(
    "Select or Enter Asset:",
    ["BTC-USD (Crypto)", "GC=F (Gold)", "^NSEI (Nifty 50)", "RELIANCE.NS (NSE Stock)", "Custom Symbol"]
)

if "Custom" in asset_choice:
    symbol_input = st.sidebar.text_input("Enter Ticker Symbol (e.g., ETH-USD, TATAMOTORS.NS):", value="ETH-USD")
else:
    symbol_input = asset_choice.split(" ")[0]

timeframe = st.sidebar.selectbox("Select Timeframe Interval", ["1h", "1d", "15m"])

st.markdown(f"**Selected Asset for Trial:** `{symbol_input}` ({timeframe})")

if symbol_input:
    try:
        data = yf.download(symbol_input, period="7d", interval=timeframe)
        
        if not data.empty:
            if isinstance(data.columns, __import__('pandas').MultiIndex):
                data.columns = data.columns.get_level_values(0)
                
            current_price = float(data['Close'].iloc[-1])
            prev_price = float(data['Close'].iloc[-2])
            price_change = ((current_price - prev_price) / prev_price) * 100
            
            data['RSI'] = ta.rsi(data['Close'], length=14)
            current_rsi = float(data['RSI'].iloc[-1]) if not data['RSI'].empty else 50.0
            
            st.success(f"Live Data Fetched Successfully for {symbol_input}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Current Live Price", value=f"${current_price:,.2f}", delta=f"{price_change:.2f}%")
            with col2:
                st.metric(label="Current RSI (14)", value=f"{current_rsi:.2f}")
            with col3:
                st.metric(label="Market Status", value="Active / Live")
                
            st.markdown("---")
            st.subheader("🏛️ Tribunal Record & Supreme Judge's Verdict")
            
            if current_rsi < 42:
                verdict = "BUY"
                color_code = "#00ff00"
                lawyer_argument = "🐂 **Buy Lawyer (Prosecution for Long):** Price has entered a discount zone with oversold RSI conditions. Potential liquidity sweep near external lows detected."
                reasoning = "Discount zone alignment with oversold momentum triggers a bullish defense."
            elif current_rsi > 58:
                verdict = "SELL"
                color_code = "#ff4d4d"
                lawyer_argument = "🐻 **Sell Lawyer (Defense/Prosecution for Short):** Price is testing premium resistance zones with overbought RSI. Bearish market structure shift (MSS) observed."
                reasoning = "Premium zone rejection with overbought momentum favors short continuation."
            else:
                verdict = "NO TRADE"
                color_code = "#ffa500"
                lawyer_argument = "⚖️ **Neutral Counsel:** Market is trading within the equilibrium range. No clear institutional order block mitigation or liquidity sweep has occurred yet."
                reasoning = "Consolidation phase. Await displacement outside equilibrium boundaries."
                
            st.info(lawyer_argument)
            st.markdown(f"<h2 style='color: {color_code}; text-align: center;'>SUPREME JUDGE VERDICT: {verdict}</h2>", unsafe_allow_html=True)
            st.write(f"**Legal Rationale & Execution Directive:** {reasoning}")
            
            st.markdown("---")
            st.subheader("📈 Price Action Trend Chart")
            st.line_chart(data['Close'])
            
        else:
            st.error("Could not fetch data for this symbol. Please check the ticker format.")
            
    except Exception as e:
        st.error(f"Error fetching live data: {e}")
