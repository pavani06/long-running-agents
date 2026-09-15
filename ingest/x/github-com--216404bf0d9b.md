---
url: "https://github.com/danny-avila/LibreChat"
key: "216404bf0d9b"
status: "ok"
final_url: "https://github.com/danny-avila/LibreChat"
method: "trafilatura"
content_hash: "036e8f868f96d86b7a9d1f0ac27fbdafae69c7e8"
text_len: 9309
fetched: "2026-09-15"
---

English · 中文
- Agent Management API (beta): Create, discover, update, and delete Agents; manage Agent files and Skills; and authenticate machine clients through deployment-bound OIDC identities while preserving existing role and Agent access controls.
- Attached workspaces (highly experimental): Select or save a per-Agent default workspace for each managed or personal code worker, then let Agents inspect trees, read and search files, author changes, and run Bash with bounded timeouts. Personal workers support bounded self-service enrollment, readiness status, and per-Agent Git identity.
- Background tool controls: Optionally cancel ordinary background tools, including attached Bash, while keeping detached Subagent execution independent.
- Code approval controls: Choose Ask, Allow, or Deny for file writes and command execution where administrators permit it, including a Full access mode for trusted attached environments. File Search and Run Code also honor role grants.
- Manual context compaction: Start a summarize-only turn before the context window fills while preserving recent conversation content according to the deployment's summarization policy.
- Context Usage: Inspect dialogue, retained tool traffic, Agent instructions, cache, cost, and runway pressure without double-counting category subsets.
- Unified attachments: Upload once and let LibreChat route content to the model or extracted text, then provision File Search and Code tools only when needed.
- Models: Added GPT-6 Astra for the OpenAI and Agents endpoints, with Responses API routing and tool-call support.
- Agent and chat UI: Unified tool activity, reasoning, search, and Agent workflows; added one draggable Pinned section for chats and favorites, morphing state icons, high-contrast themes, rich-text message copying, clearer sidebar titles, and refined live phase layouts.
- Observability: Export correlated application logs through OpenTelemetry, configure allowlisted Langfuse trace identity and metadata, tag browser diagnostics with client build IDs, and scope Insights to authorized Agents.
- Reliability and security: Strengthened Agent continuation and checkpoint recovery, Redis liveness detection, DocumentDB coordination, OpenID and MCP OAuth sessions, shared-link throttling, tenant isolation, attachment bounds, and upload error handling.
Read the full v0.8.8-rc3 changelog.
- 
🖥️ UI & Experience inspired by ChatGPT with enhanced design and features
- 
🤖 AI Model Selection: 
  - Anthropic (Claude), AWS Bedrock, OpenAI, Azure OpenAI, Google, Vertex AI, OpenAI Responses API (incl. Azure)
  - Custom Endpoints: Use any OpenAI-compatible API with LibreChat, no proxy required
  - Compatible with Local & Remote AI Providers:
    - Ollama, AMD Lemonade, groq, Cohere, Mistral AI, Apple MLX, koboldcpp, together.ai,
    - OpenRouter, Helicone, Perplexity, ShuttleAI, Deepseek, Qwen, and more
- 
🔧 Code Interpreter API: 
  - Secure, Sandboxed Execution in Python, Node.js (JS/TS), Go, C/C++, Java, PHP, Rust, and Fortran
  - Seamless File Handling: Upload, process, and download files directly
  - No Privacy Concerns: Fully isolated and secure execution
  - Open-Source & Self-Hostable: powered by ClickHouse/code-interpreter
- 
🔦 Agents & Tools Integration: 
  - LibreChat Agents:
    - No-Code Custom Assistants: Build specialized, AI-driven helpers
    - Agent Marketplace: Discover and deploy community-built agents
    - Collaborative Sharing: Share agents with specific users and groups
    - Flexible & Extensible: Use MCP Servers, tools, file search, code execution, and more
    - Skills: Create reusable SKILL.md instruction bundles for manual, automatic, or always-on agent workflows
    - Agent Plugins: Experimentally bundle deployment Skills and MCP servers into startup-loaded packages
    - Subagents: Delegate focused work to isolated child agent runs with their own context windows
    - Agent Management API: Automate Agent, file, and Skill management with deployment-bound OIDC clients
    - Attached Code Workspaces: Let Agents inspect, search, edit, and run commands in managed or personal workspaces (highly experimental)
    - Compatible with Custom Endpoints, OpenAI, Azure, Anthropic, AWS Bedrock, Google, Vertex AI, Responses API, and more
    - Model Context Protocol (MCP) Support for Tools
- LibreChat Agents:
- 
🔍 Web Search: 
  - Search the internet and retrieve relevant information to enhance your AI context
  - Combines search providers, content scrapers, and result rerankers for optimal results
  - Customizable Jina Reranking: Configure custom Jina API URLs for reranking services
  - Learn More →
- 
🪄 Generative UI with Code Artifacts: 
  - Code Artifacts create React, HTML, and Mermaid content directly in chat
  - Open previews fullscreen and export Mermaid diagrams as SVG or PNG
- 
🎨 Image Generation & Editing 
  - Text-to-image and image-to-image with GPT-Image-1
  - Text-to-image with DALL-E (3/2), Stable Diffusion, Flux, or any MCP server
  - Produce stunning visuals from prompts or refine existing images with a single instruction
- 
💾 Presets & Context Management: 
  - Create, Save, & Share Custom Presets
  - Switch between AI Endpoints and Presets mid-chat
  - Edit, Resubmit, and Continue Messages with Conversation branching
  - Create and share prompts with specific users and groups
  - Fork Messages & Conversations for Advanced Context control
  - Compact long conversations on demand while preserving recent context
- 
💬 Multimodal & File Interactions: 
  - Upload and analyze images with Claude 3, GPT-4.5, GPT-4o, o1, Llama-Vision, and Gemini 📸
  - Chat with Files using Custom Endpoints, OpenAI, Azure, Anthropic, AWS Bedrock, & Google 🗃️
  - Copy messages as formatted rich text for documents, email, and collaboration apps
- 
🌎 Multilingual UI: 
  - English, 中文 (简体), 中文 (繁體), العربية, Deutsch, Español, Français, Italiano
  - Polski, Português (PT), Português (BR), Русский, 日本語, Svenska, 한국어, Tiếng Việt
  - Türkçe, Nederlands, עברית, Català, Čeština, Dansk, Eesti, فارسی
  - Suomi, Magyar, Հայերեն, Bahasa Indonesia, ქართული, Latviešu, ไทย, ئۇيغۇرچە
- 
🧠 Reasoning UI: 
  - Dynamic Reasoning UI for Chain-of-Thought/Reasoning AI models like DeepSeek-R1
- 
🎨 Customizable Interface: 
  - Customizable Dropdown & Interface that adapts to both power users and newcomers
  - Light, dark, system, and high-contrast appearance modes
- 
📈 Observability: 
  - Export traces and logs with OpenTelemetry and connect Langfuse for Agent and model insights
- 
🌊 Resumable Streams: 
  - Never lose a response: AI responses automatically reconnect and resume if your connection drops
  - Multi-Tab & Multi-Device Sync: Open the same chat in multiple tabs or pick up on another device
  - Production-Ready: Works from single-server setups to horizontally scaled deployments with Redis
- 
🗣️ Speech & Audio: 
  - Chat hands-free with Speech-to-Text and Text-to-Speech
  - Automatically send and play Audio
  - Supports OpenAI, Azure OpenAI, and Elevenlabs
- 
📥 Import & Export Conversations: 
  - Import Conversations from LibreChat, ChatGPT, Chatbot UI
  - Export conversations as screenshots, markdown, text, json
- 
🔍 Search & Discovery: 
  - Search all messages/conversations
- 
👥 Multi-User & Secure Access: 
  - Multi-User, Secure Authentication with OAuth2, LDAP, & Email Login Support
  - Built-in Moderation, and Token spend tools
- 
🎛️ Admin Panel: 
  - Browser-based UI to manage users, groups, roles, and configuration overrides
  - Edit settings and per-role/group permissions live, without redeploying
  - Bundled with the Docker Compose stacks for one-command setup
- 
⚙️ Configuration & Deployment: 
  - Configure Proxy, Reverse Proxy, Docker, & many Deployment options
  - Use S3 with CloudFront for stable media links, edge delivery, signed cookies, and secured downloads
  - Use completely local or deploy on the cloud
- 
📖 Open-Source & Community: 
  - Completely Open-Source & Built in Public
  - Community-driven development, support, and feedback
For a thorough review of our features, see our docs here 📚
LibreChat is a self-hosted AI chat platform that unifies all major AI providers in a single, privacy-focused interface.
Beyond chat, LibreChat provides AI Agents, Model Context Protocol (MCP) support, Artifacts, Code Interpreter, custom actions, conversation search, and enterprise-ready multi-user authentication.
Open source, actively developed, and built for anyone who values control over their AI infrastructure.
GitHub Repo:
- RAG API: github.com/danny-avila/rag_api
- Website: github.com/LibreChat-AI/librechat.ai
Other:
- Website: librechat.ai
- Documentation: librechat.ai/docs
- Blog: librechat.ai/blog
Keep up with the latest updates by visiting the releases page and notes:
Contributions, suggestions, bug reports and fixes are welcome!
For new features, components, or extensions, please open an issue and discuss before sending a PR.
If you'd like to help translate LibreChat into your language, we'd love your contribution! Improving our translations not only makes LibreChat more accessible to users around the world but also enhances the overall user experience. Please check out our Translation Guide.
We thank Locize for their translation management tools that support multiple languages in LibreChat.
