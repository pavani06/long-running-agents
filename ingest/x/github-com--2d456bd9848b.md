---
url: "https://github.com/tencent/AI-Infra-Guard"
key: "2d456bd9848b"
status: "ok"
final_url: "https://github.com/tencent/AI-Infra-Guard"
method: "trafilatura"
content_hash: "58d28efeffcdfefe728b3cba827b27f3ad193e62"
text_len: 20125
fetched: "2026-09-13"
---

📖 Documentation | 🌐 🇨🇳 中文 · 🇯🇵 日本語 · 🇪🇸 Español · 🇩🇪 Deutsch · 🇫🇷 Français · 🇰🇷 한국어 · 🇧🇷 Português · 🇷🇺 Русский
A.I.G (AI-Infra-Guard) integrates capabilities such as ClawScan(OpenClaw Security Scan), Agent Scan，AI infra vulnerability scan, MCP Server & Agent Skills scan, and Jailbreak Evaluation, aiming to provide users with the most comprehensive, intelligent, and user-friendly solution for AI security risk self-examination.
We are committed to making A.I.G(AI-Infra-Guard) the industry-leading AI red teaming platform. More stars help this project reach a wider audience, attracting more developers to contribute, which accelerates iteration and improvement. Your star is crucial to us!
Help us improve A.I.G! Please take 3-5 minutes to fill out our User Feedback Survey. Users who provide high-quality feedback and leave a valid email address will receive an exclusive Tencent souvenir gift.
- 2026-09-10 · v4.6.1 — API Checker: expanded model fingerprint coverage (Gemini 2.5/3.1, Gemma 2/3/4, GLM-5.3 & GLM-5.3-Flash); MCP-Scan reliability: flags empty/incomplete scans, preserves security findings during context compaction, surfaces underlying connection errors; corrected mislabeled CVE product names.
- 2026-08-26 · v4.6.0 — LLM API poisoning detection (multi-probe black-box audit for model substitution & backdoor risks); Agent-Scan v5.0.0 mutation engine refactor; vuln library expanded to 146 AI components & 2000+ CVE rules; MCP/Skill scan stability & compatibility fixes.
- 2026-08-17 · v4.5.2 — Skill-Scan: .pyc bytecode bypass detection + charset smuggling defense; MCP-Scan: RCE prevention via tool whitelisting in dynamic mode; new SkillJack research project; vuln library expanded to 2000+ CVE rules.
- 2026-07-30 · v4.5.1 — Jailbreak Evaluation: 4 multi-turn jailbreak attacks (Many-Shot, PAIR, GOAT, ActorAttack); Agent-Scan: 5 new OWASP skills + web-exfiltration detection (10 skills total); MCP-Scan: 4 new security rules
- 2026-07-27 · v4.5.0 — AI Security Skill Market launched (3 official skills); frontend fully open-sourced; Skill scan engine upgraded (9 risk categories, SkillTrustBench top score 0.9848); Skill/MCP/Agent scan as standalone CLI; vuln library expanded to 130 components, 1888 rules
👉 Earlier releases · 🛒 AI Security Skill Market · 🔍 skill-scan CLI · 🔍 mcp-scan CLI · 🔍 agent-scan CLI · 📊 SkillTrustBench
| Docker | RAM | Disk Space | 
|---|---|---|
| 20.10 or higher | 4GB+ | 10GB+ | 
# This method pulls pre-built images from Docker Hub for a faster start
git clone https://github.com/Tencent/AI-Infra-Guard.git
cd AI-Infra-Guard
# For Docker Compose V2+, replace 'docker-compose' with 'docker compose'
docker-compose -f docker-compose.images.yml up -d
Once the service is running, you can access the A.I.G web interface at:
http://localhost:8088
You can also call A.I.G directly from OpenClaw chat via the aig-scanner skill.
clawhub install aig-scanner
Then configure AIG_BASE_URL to point to your running A.I.G service.
For more details, see the aig-scanner README.
More installation options
Method 2: One-Click Install Script （Recommended）
# This method will automatically install Docker and launch A.I.G with one command
curl https://raw.githubusercontent.com/Tencent/AI-Infra-Guard/refs/heads/main/docker.sh | bash
Method 3: Build and run from source
git clone https://github.com/Tencent/AI-Infra-Guard.git
cd AI-Infra-Guard
# This method builds a Docker image from local source code and starts the service
# (For Docker Compose V2+, replace 'docker-compose' with 'docker compose')
docker-compose up -d
Note: The AI-Infra-Guard project is positioned as an AI red teaming platform for internal use by enterprises or individuals. It currently lacks an authentication mechanism and should not be deployed on public networks.
For more information, see: https://tencent.github.io/AI-Infra-Guard/?menu=getting-started
Agent Skill security audit tool, easily integrated into enterprise CI/CD pipelines. Vulnerability classification aligns with SkillTrustBench T01–T09 taxonomy. Learn more →
pip install aig-skill-scan
# Set API key via environment variable
export LLM_API_KEY="your-api-key"
# Scan a local Skill project directory
aig-skill-scan --repo /path/to/your/skill \
           -m deepseek-v4-flash \
           --language en \
           -o result.json
The checker frontend is deployed separately. Docker deployment keeps the
checker APIs available at GET /api/v1/relay/models and
POST /api/v1/relay/check/stream; API documentation is available at
http://127.0.0.1:8088/api-checker/docs. To run the checker and unified CLI
from source:
python3 -m venv services/api_checker/.venv
services/api_checker/.venv/bin/pip install -r services/api_checker/requirements.txt
go build -o ai-infra-guard ./cmd/cli/main.go
export AIG_API_CHECKER_PYTHON="$PWD/services/api_checker/.venv/bin/python"
./ai-infra-guard api-checker list
./ai-infra-guard api-checker audit
See the API Checker integration guide for the Agent-embedded runtime architecture, HTTP API, configuration, and security boundaries.
Experience the Pro version with advanced features and improved performance. The Pro version requires an invitation code and is prioritized for contributors who have submitted issues, pull requests, or discussions, or actively help grow the community. Visit: https://aigsec.ai/.
Performance on SkillTrustBench with different LLMs:
| # | Model | F1 | Precision | Recall | FPR | 
|---|---|---|---|---|---|
| 1 | Claude Opus 4.6 | 0.9848 | 0.9725 | 0.9974 | 0.0663 | 
| 2 | GLM 5.1 | 0.9836 | 0.9701 | 0.9974 | 0.0723 | 
| 3 | Gemini 3.5 Flash | 0.9792 | 0.9947 | 0.9641 | 0.0120 | 
| 4 | Kimi 2.6 | 0.9780 | 0.9895 | 0.9667 | 0.0241 | 
| 5 | DeepSeek v4 Flash | 0.9740 | 0.9868 | 0.9615 | 0.0301 | 
Covers 9 categories of Skill security risks (SkillTrustBench T01–T09):
| Layer | Risks | 
|---|---|
| A · Instruction & Memory | T01 Skill Instruction Hijacking, T02 Memory Poisoning | 
| B · Code Execution | T03 Remote Payload Download & Execution, T04 Embedded Malicious Code | 
| C · System Privilege | T05 Privilege Escalation & Unauthorized Access, T06 System Persistence | 
| D · Toolchain & Dependencies | T07 Tool Hijacking & Spoofing, T08 Insecure Dependencies | 
| E · Skill Code Quality | T09 Insecure Coding Practices | 
For full leaderboard and details, visit SkillTrustBench.
| Feature | More Info | 
|---|---|
| ClawScan(OpenClaw Security Scan) | Supports one-click evaluation of OpenClaw security risks. It detects insecure configurations, Skill risks, CVE vulnerabilities, and privacy leakage. | 
| Agent Scan | This is an independent, multi-agent automated scanning framework. It is designed to evaluate the security of AI agent workflows. It seamlessly supports agents running across various platforms, including Dify and Coze. | 
| MCP Server & Agent Skills scan | It thoroughly detects 14 major categories of security risks. The detection applies to both MCP Servers and Agent Skills. It flexibly supports scanning from both source code and remote URLs. | 
| AI infra vulnerability scan | This scanner precisely identifies over 100 AI framework components. It covers more than 2000 known CVE vulnerabilities. Supported frameworks include Ollama, ComfyUI, vLLM, n8n, Triton Inference Server and more. | 
| Jailbreak Evaluation | It assesses prompt security risks using carefully curated datasets. The evaluation applies multiple attack methods to test robustness. It also provides detailed cross-model comparison capabilities. | 
| Model and API Relay Checker | Model fingerprinting, Claude Signature verification, relay black-box auditing, PAMELA, and Ventor QTest. | 
💎 Additional Benefits
- 🖥️ Modern Web Interface: User-friendly UI with one-click scanning and real-time progress tracking
- 🔌 Complete API: Full interface documentation and Swagger specifications for easy integration
- 🤖 Agent-Ready: Plug-and-play agent skills on ClawHub — EdgeOne ClawScan, EdgeOne Skill Scanner, and AIG Scanner — seamlessly embed security scanning into any AI agent workflow
- 🌐 Multi-Language: Chinese and English interfaces with localized documentation
- 🐳 Cross-Platform: Linux, macOS, and Windows support with Docker-based deployment
- 🆓 Free & Open Source: Completely free under the Apache 2.0 license
After deployment, open http://localhost:8088 in your browser.
What to enter as the target URL / IP?
The target is the network address of a running AI service you want to scan - not a GitHub URL or source code path. A.I.G connects to the live service and fingerprints it for known CVE vulnerabilities.
| Scenario | Example target | 
|---|---|
| A locally running vLLM instance | http://127.0.0.1:8000 | 
| An Ollama server on your LAN | http://192.168.1.100:11434 | 
| A ComfyUI instance exposed internally | http://10.0.0.5:8188 | 
| Multiple hosts (one per line) | 192.168.1.0/24 (CIDR),10.0.0.1-10.0.0.20 (range) | 
Step-by-step: Scan a local vLLM instance
- Start vLLM normally (e.g. python -m vllm.entrypoints.api_server --model meta-llama/... )
- In the A.I.G web UI, click "AI基础设施安全扫描 / AI Infra Scan"
- Enter http://127.0.0.1:8000 (or the IP/port where vLLM is listening)
- Click Start Scan - A.I.G will fingerprint the service and match it against 2000+ known CVEs
- View the report: component version, matched vulnerabilities, severity, and remediation links
💡 Tip: To scan the nightly build of vLLM specifically, just run that nightly build and point A.I.G at its address. The scanner detects the version automatically.
Enter either a remote URL (e.g. https://github.com/user/mcp-server) or upload a local source archive - no running instance required.
Configure the target LLM's API endpoint (base URL + API key) in Settings → Model Config, then select a dataset and start the evaluation.
Visit our online documentation: https://tencent.github.io/AI-Infra-Guard/
For more detailed FAQs and troubleshooting guides, visit our documentation.
A.I.G provides a comprehensive set of task creation APIs that support AI infra scan, MCP Server Scan, and Jailbreak Evaluation capabilities.
After the project is running, visit http://localhost:8088/docs/index.html to view the complete API documentation.
For detailed API usage instructions, parameter descriptions, and complete example code, please refer to the Complete API Documentation.
The extensible plugin framework serves as A.I.G's architectural cornerstone, inviting community innovation through Plugin and Feature contributions.
- Fingerprint Rules: Add new YAML fingerprint files to the data/fingerprints/ directory.
- Vulnerability Rules: Add new vulnerability scan rules to the data/vuln/ directory.
- MCP Plugins: Add new MCP security scan rules to the data/mcp/ directory.
- Jailbreak Evaluation Datasets: Add new Jailbreak evaluation datasets to the data/eval directory.
Please refer to the existing rule formats, create new files, and submit them via a Pull Request.
This project is led and developed by Tencent Zhuque Lab, part of the Tencent Security Platform Department. Founded in 2019, Tencent Zhuque Lab is a top-tier security research lab focused on real-world offensive and defensive research and frontier technology in the AI security space, covering large model security, AI agent security, AI-empowered security, and AI-generated content detection.
The team has helped major vendors such as NVIDIA, Google, and Microsoft, as well as open-source communities like OpenClaw, Linux, and Hugging Face, fix a large number of high-risk vulnerabilities, and has been publicly acknowledged by them.
We have released open-source AI security products including the AI Red Team Security Testing Platform A.I.G (AI-Infra-Guard) and the Zhuque AI Detection Assistant. Our research has been widely published at top international security and AI conferences such as Black Hat, DEF CON, ICLR, CVPR, NeurIPS, and ACL, and we have authored the book "AI Security: Technology and Practice".
| Role | Member | Contribution | 
|---|---|---|
| Head of Tencent Security Platform Department | Yong Yang | Initiated A.I.G and proposed automated assessment of AI agent loss-of-control risks, guiding the platform's expansion from AI infrastructure vulnerability scanning to agent execution risk, tool misuse, and permission-boundary evaluation. | 
| Head of Tencent Zhuque Lab | Xing Zheng | Proposed the automated vulnerability-update and benchmark-alignment mechanism, helping AI Infra fingerprints, CVE/GHSA rules, and benchmarks iterate continuously. | 
| Project Lead | Nicky | Frontier security research, product planning, technical-route decisions, internal and external collaboration, and communications. | 
| Technical Lead | Python | Overall architecture design, core module development, and version iteration. | 
| Core Contributor | Zona | Frontend interaction, product experience, community operations, and user-feedback loop. | 
| Core Contributor | Fyoung | AI Infra vulnerability component fingerprint updates and Benchmark system construction. | 
| Core Contributor | Xiangfan | Security capability development for Skill risks and agent loss-of-control scenarios. | 
| Core Contributor | Elwood | Enhancing Agent security scanning capabilities and updating technical reports. | 
| Core Contributor | Robert | LLM safety assessment and jailbreak-evaluation strategy operations. | 
| Core Contributor | Zoe | LLM safety assessment, jailbreak evaluation, and model-integration module development. | 
| Contributor | Ronin | Participated in AI agent security scanning development. | 
| Contributor | Rsin | Participated in community operations and campaign communications. | 
We thank our academic partners for their research contributions and technical support.
| Prof. hui Li | Bin Wang | Zexin Liu | Hao Yu | Ao Yang | Zhengxi Lin | 
| Prof. Zhemin Yang | Kangwei Zhong | Jiapeng Lin | Cheng Sheng | 
Thanks to all the developers who have contributed to the A.I.G project.
Thanks to the users from the following organizations and teams for using A.I.G and their valuable feedback.
- GitHub Discussions: Join our community discussions
- Issues & Bug Reports: Report issues or suggest features
| WeChat Group | Discord [link] | 
|---|---|
For collaboration inquiries or feedback, please contact us at: zhuque@tencent.com
If you are interested in code security, check out A.S.E (AICGSecEval), the industry's first repository-level AI-generated code security evaluation framework open-sourced by the Tencent Wukong Code Security Team.
If you use A.I.G in your research, please cite:
@misc{Tencent_AI-Infra-Guard_2025,
  author={{Tencent Zhuque Lab}},
  title={{AI-Infra-Guard: A Comprehensive, Intelligent, and Easy-to-Use AI Red Teaming Platform}},
  year={2025},
  howpublished={GitHub repository},
  url={https://github.com/Tencent/AI-Infra-Guard}
}
Research:
- 
"DeepSeek Harness Indirect Prompt-Injection Assessment" — Authorized security assessment of DeepSeek Harness against indirect prompt-injection across 14,560 agent runs. [code]
- 
"SkillJack: Persistent Skill Backdoors in Self-Evolving Agents" — Demonstrates how poisoned trajectories can inject persistent backdoors into self-evolving agent skill systems. [code]
Papers:
- 
"Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming" — A comprehensive framework for securing AI agent systems through multi-layer red teaming across infrastructure, supply chain, runtime interaction, and deployment surfaces. [arXiv] [pdf]
- 
"AI-Infra-Guard: An AI Red Teaming Platform" — Black Hat Europe 2025 Arsenal presentation showcasing A.I.G's capabilities and real-world use cases. [pdf]
- 
"MCP Unchained: Compromising The AI Agent Ecosystem Via Its Universal Connector" — Black Hat Europe 2025 talk revealing security risks in the MCP protocol within the AI agent ecosystem. [pdf]
Thanks to the research teams who have cited A.I.G in their academic work (19 papers):
📄 View all 19 cited papers
- 
Chenning Li, Pan Hu, Justin Xu et al. "ADR: An Agentic Detection System for Enterprise Agentic AI Security." arXiv preprint arXiv:2605.17380 (2026). [pdf]
- 
Zhaojiacheng Zhou. "Proteus: A Self-Evolving Red Team for Agent Skill Ecosystems." arXiv preprint arXiv:2605.11891 (2026). [pdf]
- 
Hengkai Ye, Zhechang Zhang, Jinyuan Jia et al. "TRUSTDESC: Preventing Tool Poisoning in LLM Applications via Trusted Description Generation." arXiv preprint arXiv:2604.07536 (2026). [pdf]
- 
Zenghao Duan, Yuxin Tian, Zhiyi Yin et al. "SkillAttack: Automated Red Teaming of Agent Skills through Attack Path Refinement." arXiv preprint arXiv:2604.04989 (2026). [pdf]
- 
Yiheng Huang, Zhijia Zhao, Bihuan Chen et al. "From Component Manipulation to System Compromise: Understanding and Detecting Malicious MCP Servers." arXiv preprint arXiv:2604.01905 (2026). [pdf]
- 
Yi Ting Shen, Kentaroh Toyoda, Alex Leung. "MCP-38: A Comprehensive Threat Taxonomy for Model Context Protocol Systems (v1.0)." arXiv preprint arXiv:2603.18063 (2026). [pdf]
- 
Yuepeng Hu, Yuqi Jia, Mengyuan Li et al. "MalTool: Malicious Tool Attacks on LLM Agents." arXiv preprint arXiv:2602.12194 (2026). [pdf]
- 
Naen Xu, Jinghuai Zhang, Ping He et al. "FraudShield: Knowledge Graph Empowered Defense for LLMs against Fraud Attacks." arXiv preprint arXiv:2601.22485v1 (2026). [pdf]
- 
Ruiqi Li, Zhiqiang Wang, Yunhao Yao et al. "MCP-ITP: An Automated Framework for Implicit Tool Poisoning in MCP." arXiv preprint arXiv:2601.07395v1 (2026). [pdf]
- 
Jingxiao Yang, Ping He, Tianyu Du et al. "HogVul: Black-box Adversarial Code Generation Framework Against LM-based Vulnerability Detectors." arXiv preprint arXiv:2601.05587v1 (2026). [pdf]
- 
Teofil Bodea, Masanori Misono, Julian Pritzi et al. "Trusted AI Agents in the Cloud." arXiv preprint arXiv:2512.05951v1 (2025). [pdf]
- 
Yunyi Zhang, Shibo Cui, Baojun Liu et al. "Beyond Jailbreak: Unveiling Risks in LLM Applications Arising from Blurred Capability Boundaries." arXiv preprint arXiv:2511.17874v2 (2025). [pdf]
- 
Bin Wang, Zexin Liu, Hao Yu et al. "MCPGuard: Automatically Detecting Vulnerabilities in MCP Servers." arXiv preprint arXiv:2510.23673v1 (2025). [pdf]
- 
Weibo Zhao, Jiahao Liu, Bonan Ruan et al. "When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation." arXiv preprint arXiv:2509.24272v1 (2025). [pdf]
- 
Ping He, Changjiang Li, et al. "Automatic Red Teaming LLM-based Agents with Model Context Protocol Tools." arXiv preprint arXiv:2509.21011 (2025). [pdf]
- 
Christian Coleman. "Behavioral Detection Methods for Automated MCP Server Vulnerability Assessment." (2025). [pdf]
- 
Yixuan Yang, Daoyuan Wu, Yufan Chen. "MCPSecBench: A Systematic Security Benchmark and Playground for Testing Model Context Protocols." arXiv preprint arXiv:2508.13220 (2025). [pdf]
- 
Yongjian Guo, Puzhuo Liu, et al. "Systematic Analysis of MCP Security." arXiv preprint arXiv:2508.12538 (2025). [pdf]
- 
Zexin Wang, Jingjing Li, et al. "A Survey on AgentOps: Categorization, Challenges, and Future Directions." arXiv preprint arXiv:2508.02121 (2025). [pdf]
📧 If you have used A.I.G in your research or product, or if we have inadvertently missed your publication, we would love to hear from you! Contact us here.
This project is open-sourced under the Apache License 2.0. We warmly welcome and encourage community contributions, integrations, and derivative works, subject to the following attribution requirements:
- Retain notices: You must retain the LICENSE andNOTICE files from the original project in any distribution.
- Product attribution: If you integrate AI-Infra-Guard's core code, components, or scanning engine into your open-source project, commercial product, or internal platform, you must clearly state the following in your product documentation, usage guide, or UI "About" page:
"This project integrates AI-Infra-Guard, open-sourced by Tencent Zhuque Lab."
- Academic & article citation: If you use this tool in vulnerability analysis reports, security research articles, or academic papers, please explicitly mention "Tencent Zhuque Lab AI-Infra-Guard" and include a link to the repository.
Repackaging this project as an original product without disclosing its origin is strictly prohibited.
