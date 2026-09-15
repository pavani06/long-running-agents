---
url: "https://github.com/TauricResearch/TradingAgents"
key: "1606cfe2c2a9"
status: "ok"
final_url: "https://github.com/TauricResearch/TradingAgents"
method: "trafilatura"
content_hash: "aaf79f0c17b39750592e15a8ef7b897fc20fb1e9"
text_len: 13478
fetched: "2026-09-15"
---

- [2026-08] TradingAgents v0.4.0 released with look-ahead / point-in-time fixes across FRED macro, social sentiment, and the decision-log memory; clearer decision signals; working CLI checkpoint resume; Trader price grounding; and the GPT-5.6 and GLM-5.3 models. See CHANGELOG.md for the full list.
- [2026-07] TradingAgents v0.3.1 released with correctness and stability fixes: Alpha Vantage look-ahead filtering, graph-router crash-safety, graph-shape-aware checkpoint resume, working crypto sentiment sources, a configurable LLM retry budget, Bedrock API-key auth, and Claude Sonnet 5 / Fable 5 support.
- [2026-06] TradingAgents v0.3.0 released with a verified data-access contract, an expanded provider registry (NVIDIA, Kimi, Groq, Mistral, Bedrock, and any OpenAI-compatible endpoint), FRED and Polymarket data vendors, a current-generation model catalog, and a CI gate.
- [2026-05] TradingAgents v0.2.5 released with the grounded Sentiment Analyst, GPT-5.5 etc. model coverage, Qwen/GLM/MiniMax dual-region support, TRADINGAGENTS_* env-var configurability with API-key auto-detection, remote Ollama support, non-US alpha benchmarks, and ticker path-traversal hardening.
- [2026-04] TradingAgents v0.2.4 released with structured-output agents (Research Manager, Trader, Portfolio Manager), LangGraph checkpoint resume, persistent decision log, DeepSeek/Qwen/GLM/Azure provider support, Docker, and a Windows UTF-8 encoding fix.
- [2026-03] TradingAgents v0.2.3 released with multi-language support, GPT-5.4 family models, unified model catalog, backtesting date fidelity, and proxy support.
- [2026-03] TradingAgents v0.2.2 released with GPT-5.4/Gemini 3.1/Claude 4.6 model coverage, five-tier rating scale, OpenAI Responses API, Anthropic effort control, and cross-platform stability.
- [2026-02] TradingAgents v0.2.0 released with multi-provider LLM support (GPT-5.x, Gemini 3.x, Claude 4.x, Grok 4.x) and improved system architecture.
- [2026-01] Trading-R1 Technical Report released, with Terminal expected to land soon.
🚀 TradingAgents | ⚡ Installation & CLI | 🎬 Demo | 📦 Package Usage | 🤝 Contributing | 📄 Citation
🎉 TradingAgents officially released! We have received numerous inquiries about the work, and we would like to express our thanks for the enthusiasm in our community.
So we decided to fully open-source the framework. Looking forward to building impactful projects with you!
TradingAgents is a multi-agent trading framework that mirrors the dynamics of real-world trading firms. By deploying specialized LLM-powered agents: from fundamental analysts, sentiment experts, and technical analysts, to trader, risk management team, the platform collaboratively evaluates market conditions and informs trading decisions. Moreover, these agents engage in dynamic discussions to pinpoint the optimal strategy.
TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. It is not intended as financial, investment, or trading advice.
Our framework decomposes complex trading tasks into specialized roles.
- Fundamentals Analyst: Evaluates company financials and performance metrics, identifying intrinsic values and potential red flags.
- Sentiment Analyst: Aggregates news headlines, StockTwits, and Reddit chatter into a single sentiment read to gauge short-term market mood.
- News Analyst: Monitors global news and macroeconomic indicators, interpreting the impact of events on market conditions.
- Technical Analyst: Utilizes technical indicators (like MACD and RSI) to detect trading patterns and forecast price movements.
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.
- Composes reports from the analysts and researchers to make informed trading decisions, determining the timing and magnitude of trades.
- Continuously evaluates portfolio risk by assessing market volatility, liquidity, and other risk factors. The risk management team evaluates and adjusts trading strategies, providing assessment reports to the Portfolio Manager for final decision.
- The Portfolio Manager approves/rejects the transaction proposal. If approved, the order will be sent to the simulated exchange and executed.
Clone TradingAgents:
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
Create a virtual environment in any of your favorite environment managers:
conda create -n tradingagents python=3.12
conda activate tradingagents
Install the package and its dependencies:
pip install .
Alternatively, run with Docker:
cp .env.example .env  # add your API keys
docker compose run --rm tradingagents
For local models with Ollama:
docker compose --profile ollama run --rm tradingagents-ollama
TradingAgents supports multiple LLM providers. Set the API key for your chosen provider:
export OPENAI_API_KEY=...          # OpenAI (GPT)
export GOOGLE_API_KEY=...          # Google (Gemini)
export ANTHROPIC_API_KEY=...       # Anthropic (Claude)
export XAI_API_KEY=...             # xAI (Grok)
export DEEPSEEK_API_KEY=...        # DeepSeek
export DASHSCOPE_API_KEY=...       # Qwen — International (dashscope-intl.aliyuncs.com)
export DASHSCOPE_CN_API_KEY=...    # Qwen — China (dashscope.aliyuncs.com)
export ZHIPU_API_KEY=...           # GLM via Z.AI (international)
export ZHIPU_CN_API_KEY=...        # GLM via BigModel (China, open.bigmodel.cn)
export MINIMAX_API_KEY=...         # MiniMax — Global (api.minimax.io)
export MINIMAX_CN_API_KEY=...      # MiniMax — China (api.minimaxi.com)
export OPENROUTER_API_KEY=...      # OpenRouter
export ALPHA_VANTAGE_API_KEY=...   # Alpha Vantage
For Azure OpenAI, copy .env.enterprise.example to .env.enterprise and fill in your credentials.
For AWS Bedrock, install the extra with pip install ".[bedrock]", set llm_provider: "bedrock", configure AWS credentials (environment variables, ~/.aws/credentials, or an IAM role) and AWS_DEFAULT_REGION, and use a Bedrock model ID, e.g. us.anthropic.claude-opus-4-8-v1:0.
For local models, configure Ollama with llm_provider: "ollama". The default endpoint is http://localhost:11434/v1; set OLLAMA_BASE_URL to point at a remote ollama-serve. Pull models with ollama pull <name>, and pick "Custom model ID" in the CLI for any model not listed by default.
For any other OpenAI-compatible server (vLLM, LM Studio, llama.cpp, or a custom relay), use llm_provider: "openai_compatible" and set the endpoint via backend_url (or TRADINGAGENTS_LLM_BACKEND_URL), e.g. http://localhost:8000/v1 for vLLM or http://localhost:1234/v1 for LM Studio. The model is whatever your server serves. No key is needed for local servers; set OPENAI_COMPATIBLE_API_KEY when the endpoint requires one.
Alternatively, copy .env.example to .env and fill in your keys:
cp .env.example .env
Launch the interactive CLI:
tradingagents          # installed command
python -m cli.main     # alternative: run directly from source
You will see a screen where you can select your desired tickers, analysis date, LLM provider, research depth, and more.
TradingAgents works with any market Yahoo Finance covers, using the exchange-suffixed ticker. Company identity and the alpha benchmark resolve automatically per market.
- US: AAPL ,SPY
- Hong Kong: 0700.HK · Tokyo:7203.T · London:AZN.L
- India: RELIANCE.NS ,.BO · Canada:.TO · Australia:.AX
- China A-shares: Shanghai .SS , Shenzhen.SZ (e.g.600519.SS for Kweichow Moutai)
- Crypto: BTC-USD ,ETH-USD
An interface will appear showing results as they load, letting you track the agent's progress as it runs.
We built TradingAgents with LangGraph to ensure flexibility and modularity. The framework supports multiple LLM providers: OpenAI, Google, Anthropic, xAI, DeepSeek, Qwen (Alibaba DashScope, international and China endpoints), GLM (Zhipu), MiniMax (global + China), OpenRouter, Ollama for local models, and Azure OpenAI for enterprise.
To use TradingAgents inside your code, you can import the tradingagents module and initialize a TradingAgentsGraph() object. The .propagate() function will return a decision. You can run main.py, here's also a quick example:
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
# forward propagate
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
You can also adjust the default configuration to set your own choice of LLMs, debate rounds, etc.
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"        # e.g. openai, google, anthropic, deepseek, groq, ollama; openai_compatible covers any OpenAI-compatible endpoint (vLLM, LM Studio, llama.cpp, ...)
config["deep_think_llm"] = "gpt-5.6"      # Model for complex reasoning
config["quick_think_llm"] = "gpt-5.6-luna" # Model for quick tasks
config["max_debate_rounds"] = 2
ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
See tradingagents/default_config.py for all configuration options.
TradingAgents persists two kinds of state across runs.
The decision log is always on. Each completed run appends its decision to ~/.tradingagents/memory/trading_memory.md. On the next run for the same ticker, TradingAgents fetches the realised return (raw and alpha vs SPY), generates a one-paragraph reflection, and injects the most recent same-ticker decisions plus recent cross-ticker lessons into the Portfolio Manager prompt, so each analysis carries forward what worked and what didn't.
Override the path with TRADINGAGENTS_MEMORY_LOG_PATH.
Checkpoint resume is opt-in via --checkpoint. When enabled, LangGraph saves state after each node so a crashed or interrupted run resumes from the last successful step instead of starting over. On a resume run you will see Resuming from step N for <TICKER> on <date> in the logs; on a new run you will see Starting fresh. Checkpoints are cleared automatically on successful completion.
Per-ticker SQLite databases live at ~/.tradingagents/cache/checkpoints/<TICKER>.db (override the base with TRADINGAGENTS_CACHE_DIR). Use --clear-checkpoints to reset all of them before a run.
tradingagents analyze --checkpoint           # enable for this run
tradingagents analyze --clear-checkpoints    # reset before runningconfig = DEFAULT_CONFIG.copy()
config["checkpoint_enabled"] = True
ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
TradingAgents is LLM-driven, so two runs of the same ticker and date can differ. This is expected for a research tool built on language models, not a defect. The variation comes from a few distinct sources, and it helps to separate them.
Language model sampling is non-deterministic. Even at a fixed temperature, providers do not guarantee byte-identical output across calls, and reasoning models (the default GPT-5.x family, and any thinking-mode model) vary the most because their internal reasoning is itself sampled.
Live data moves. News, StockTwits, and Reddit return different content as time passes, so a run today sees different inputs than a run last week even for the same historical trade date. Pin the analysis date to hold the price and indicator window fixed, but the social and news sources still reflect "now".
To reduce variation you can lower the sampling temperature. Set temperature in your config (or TRADINGAGENTS_TEMPERATURE in .env); lower values make models that honor it more repeatable. The current curated models are reasoning-first and largely ignore temperature, so for tighter reproducibility use a non-reasoning model, which you can set explicitly via the Custom model ID option.
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
config["temperature"] = 0.0
# Reasoning models ignore temperature. For tighter reproducibility, set a
# non-reasoning deep/quick model explicitly (e.g. via the Custom model ID option).
What does not vary anymore: the analyzed company identity is resolved deterministically from the ticker before any agent runs, and the market analyst grounds exact price and indicator claims in a verified data snapshot. Earlier reports of "different companies" or fabricated price levels across runs are addressed by these two mechanisms.
Backtest results are not guaranteed to match any published figure. Returns depend on the model, the temperature, the date range, data quality, and the sampling above. Treat the framework as a research scaffold for studying multi-agent analysis, not as a strategy with a fixed, replicable return.
Contributions are welcome: bug fixes, documentation, and feature ideas; past contributions are credited per release in CHANGELOG.md.
Please reference our work if you find TradingAgents provides you with some help :)
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
