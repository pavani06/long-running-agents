---
url: "https://www.uber.com/us/en/blog/uber-eats-search-pipeline/"
key: "15c3f33e67f3"
status: "ok"
final_url: "https://www.uber.com/us/en/blog/uber-eats-search-pipeline/"
method: "trafilatura"
content_hash: "915e7978bcfeaf840e3e01b8f740ca9b7434ac1c"
text_len: 16778
fetched: "2026-09-13"
---

Halving the Time: How Uber Eats Rebuilt Its Search Pipeline
Distinguished Engineer
Staff Software Engineer, TLM
Staff Software Engineer
Introduction
When someone opens Uber Eats and types a query, they aren’t waiting for a network response. They’re waiting for food. Every millisecond of search latency is product latency—it affects conversion, session depth, and whether they order at all. Our system’s search latency had grown to untenable levels. This post is about how we cut it in half—across multiple parallel workstreams spanning the full stack—and outlines the architectural changes we’re undertaking to unlock a seamless, industry-leading end-to-end experience.
The Problem
Retrieval was fetching tens of thousands of candidates and sending all of them through full hydration before ranking would discard most of them. Hydration was monolithic—a single phase that blocked both ranking and presentation in series. And the DAG (directed acrylic graph) wiring had false dependencies: steps waiting on outputs they didn’t actually need, serializing work that could have been parallel. The result was a pipeline where the bottlenecks were invisible until you measured them at the right granularity.
What We Changed
UX
Search latency is a full-stack problem, and some of our largest wins came from rethinking what we send to the UX rather than just how fast we compute it.
We shifted our primary latency metric from back-end API response time to ATF (Above-the-Fold) completion: the time from query submission to when the first screen of results is fully rendered with images in the viewport. API latency can improve while someone sees no difference if the bottleneck is in payload transfer, template rendering, or image loading. ATF forced us to optimize the entire path.
Previously, every search request rendered the full result set before the person saw anything. We introduced pagination with a server-side cache: the presentation layer returns a smaller initial page, while caching remaining results for scroll requests, avoiding recomputation.
Our HTML template rendering pipeline processed each result item sequentially, so rendering time scaled linearly with page size. We moved to an async pipeline where items render concurrently, and to support the higher per-request parallelism, we vertically scaled the presentation service. Async rendering coupled with pagination delivered an over 200 millisecond improvement in ATF latency.
Retrieval
A significant portion of our search latency originated in the retrieval layer, where multiple retrieval strategies worked in parallel to balance precision and recall.
Through offline analysis and online experimentation, we found that several broad-recall lexical retrieval strategies were adding substantial latency while contributing little incremental value. Many of the relevant results they surfaced were already being retrieved through other sources, including semantic retrieval systems. By removing these low-yield retrieval paths, we reduced end-to-end search latency by approximately 120 milliseconds without measurable regressions in conversion or result quality.
We also improved efficiency through earlier deduplication of chain stores, reducing downstream processing while creating opportunities for a broader set of relevant results to be surfaced.
Finally, we improved feature fetching efficiency by leveraging product-level embeddings to group similar items around the same products. By grouping items by their shared product identity, we reduced data lookups by over 100 times, cut retrieval latency by 50 milliseconds, and made it feasible to serve the data entirely from memory.
Taken together, these retrieval optimizations significantly improved search responsiveness while preserving result quality and relevance.
Feature Population and Ranking
A major source of latency was unnecessary work and synchronization in the ranking pipeline. Historically, ranking waited for a monolithic feature hydration phase that fetched both ranking signals and presentation data. This meant ranking couldn’t begin until every candidate had been fully hydrated, including display attributes such as prices, promotions, and stock status that weren’t required for scoring.
To address this, we split hydration into two parallel phases. Ranking hydration retrieves only the signals required for scoring, while presentation hydration fetches display-layer attributes asynchronously. This removed non-essential data from the critical path, allowing ranking to start earlier and reducing end-to-end latency by 100+ milliseconds. The split also created a cleaner architecture where ranking and presentation data can evolve independently.
We also audited the execution graph and eliminated false dependencies that had accumulated over time. Some stages were waiting on the completion of prior stages despite having no true data dependency. By parallelizing item ranking and hydration, we reduced latency by approximately 35 milliseconds. We also worked with the Search ML team to remove live item-signal dependencies from our store ranking model, allowing store and item ranking to execute independently and targeting an additional 20 milliseconds in latency reduction.
To reduce tail latency, we introduced request hedging across four presentation hydration dependency layers. When a request exceeds a latency threshold, a duplicate request is sent to another instance and the faster response is used. Because hydration latency was primarily driven by isolated shard jitter rather than correlated slowdowns, hedging proved highly effective, reducing aggregate hydration latency by 40 milliseconds.
We also upgraded our ranking infrastructure with GPU model serving, a relevance-model cache, and more efficient feature delivery. These changes reduced scoring latency, lowered model-serving costs, and further improved overall search responsiveness.
Looking ahead, while we have made solid progress on real-time features hydration, we are also working to move offline feature fetches earlier in the pipeline. Today these run sequentially after real-time features are hydrated and before model scoring can begin; we are working to run them in parallel with other hydration activities, removing them from the critical path. Beyond scheduling, we are optimizing how data is laid out in the underlying storage systems for these features to reduce fanout, as well as how feature tensors are transferred to GPU with minimal transport cost.
Ads Serving
The ads subsystem had a data layout problem. Each query processes hundreds of bids, each with many scoring components. The data was originally stored in a row-oriented format that repeated component metadata for every bid, creating significant serialization and deserialization overhead.
We redesigned the data layout into a column-oriented representation that better matched the scoring access pattern. This reduced memory overhead, in addition we moved all ad-specific data (campaigns, pacing etc) into application memory, instead of needing a DB call. This improved processing efficiency, saving approximately 30 milliseconds in ad selection and 110 milliseconds in bid preparation.
We also identified several unnecessary serialization and deserialization cycles between internal components. Eliminating these redundant conversions removed another 20 milliseconds of latency. Finally, we filtered unused scoring fields before transmission, further reducing processing costs.
The above ads optimizations combined delivered approximately 130 milliseconds of end-to-end latency reduction.
Sweating the Details: Infrastructure Tuning
Not all improvements came from major architectural changes. Profiling uncovered several infrastructure-level inefficiencies that, while unrelated to search logic, collectively reduced end-to-end latency by approximately 200 milliseconds.
When returning large result sets, the system encoded each item sequentially, leaving most CPU cores idle. We split results into independent chunks that can be encoded and decoded in parallel, reducing end-to-end latency by over 50 milliseconds.
We also found that ML embeddings power search relevance but are expensive to fetch at scale. By reducing floating-point precision to 5 decimal places and using compact variable-length integer encoding, we cut embedding size by 46% and halved the database query latency.
Our service mesh also uses a single network connection per destination with a fixed cap on concurrent in-flight requests. High-throughput services were silently hitting this cap, causing requests to queue. Opening multiple parallel connections eliminated the bottleneck, reducing latency by up to 53%.
Finally, in Go, pointer-referenced objects are heap-allocated and must be cleaned up by the garbage collector—which was consuming over 40% of CPU in some services. By switching our data model definitions to value types, these objects are stack-allocated instead, dramatically reducing GC overhead and freeing CPU for actual request processing.
Agentic Loop
One of the more unexpected workstreams was using an agentic AI loop to find and fix latency problems directly. We built a workflow where we gave an AI coding agent a latency savings target along with a set of custom engineering tools—the ability to pull live production latency profiles, identify the top bottlenecks by span, draft code fixes for the most promising ones, open pull requests, and run latency benchmarks to validate improvements before merging. The loop ran iteratively: measure → identify → fix → validate, repeating until the savings target was met or the marginal return on each additional fix fell below a threshold.
A key enabler was fast verification. We invested in an LLM-assisted evaluation framework that could quickly validate that latency improvements didn’t degrade search quality, dramatically reducing evaluation time and allowing the optimization loop to iterate much faster.
The agentic approach was most effective on a class of problems that are individually uninspiring but compound meaningfully at scale: redundant work on the critical path, metric emits that block instead of running asynchronously, unnecessary config fetches in the query loop, and hot-path allocation patterns that drive GC pauses. These are the kinds of wins that are consistently present in production profiles but rarely make it onto a roadmap.
The benchmark integration meant each fix had a measured result before merging—no speculation, just a tight loop between observation, verification, and code change.
What’s Next?
Cutting latency in half was a waypoint. The northstar is a best-in-class end-to-end experience—a bar that industry benchmarks show is achievable. Below we discuss some of the bets in flight.
End-to-End Microbatching
Today, the search pipeline operates in stages: retrieval completes before hydration begins, and hydration completes before ranking begins. This creates synchronization barriers where fast shards must wait for the slowest shard at each stage, amplifying tail latency.
To address this issue, we’re re-architecting our search pipeline with microbatching. With microbatching, candidates begin flowing through downstream stages as soon as they’re available, allowing retrieval, hydration, and ranking to overlap rather than execute in strict sequence.
By reducing waiting between stages, end-to-end latency moves closer to average shard latency instead of being dictated by the slowest shard. We estimate a potential reduction of over 100 milliseconds, along with lower latency variance.
Product-Based Search
Today, retrieval and hydration operate at the item level. While the Uber Eats catalog contains approximately a few billion items, many are store-specific variants of the same underlying product. At the product level, the catalog shrinks by roughly 100 times.
By shifting retrieval and hydration to products, we dramatically reduce the amount of data processed throughout the search pipeline. Early testing has already shown more than a 50% reduction in p99 latency.
A smaller corpus also allows us to retrieve more candidates within the same latency budget, improving recall and creating headroom for more advanced ranking signals. Product-based search improves both efficiency and result quality, making it a key part of our path to lower-latency search.
ZPR (Zero Pass Ranking)
Today, retrieval gathers a large set of candidates, and ranking later determines which results are worth keeping. ZPR (Zero-Pass Ranking) pushes part of that filtering into the index layer itself, allowing candidates to be scored and filtered as they are retrieved.
By removing lower-value candidates earlier, ZPR reduces the amount of work performed by downstream enrichment and ranking stages. Our first milestone targets roughly 30 milliseconds of latency reduction through early filtering, while the longer-term vision could unlock 50 milliseconds or more.
ZPR also complements microbatching, allowing candidates to begin flowing through downstream stages earlier and further reducing end-to-end latency.
Streaming
Today, the presentation layer blocks on generating the full page before sending anything. The Uber Eats user waits for the slowest item to render before seeing any result.
With streaming using HTTP multi-part responses, the server flushes individual result fragments as they become available. The browser renders above-the-fold content immediately while slower results (below-fold cards and carousels) stream in afterward. Where pagination reduced response size and parallel rendering reduced assembly time, fragment streaming will eliminate the requirement to render everything before flushing and subsequently rendering on the client.
Conclusion
Reducing search latency at Uber scale required improvements across the entire stack. One of the biggest accelerators was using agentic engineering workflows. By combining observability, code generation, benchmarking, and evaluation into a tight feedback loop, we could identify, validate, and ship optimizations much faster.
Just as important was our investment in measurement. We expanded tracing coverage, built detailed latency dashboards, and added automated monitoring to quickly identify bottlenecks and measure the impact of every change.
The work isn’t finished. Our next investments follow the same philosophy: do less work, start work earlier, and measure continuously.
We cut latency in half. We intend to do it again.
Acknowledgments
It truly took a village, and we had contributions from many different teams across the company to make this happen. Specifically we would like to thank the following team members: Abhi Khune, Alan Raddatz, Anuj Mehta, Ashish Gandhi, Ashish Gupta, Bilal Rizvi, Brandon Eum, Brian Hartley, Chris Miller, Chang Wang, Charles Hagma, Deval Shah, Dharini Murugaprabhu, Dohyung Park, Dongmin Zhang, Hemanth S A, Huiren Li, Jack Li, Yichen Zhou, Konstantin Vlasov, Kunal Veera, Kusha Kapoor, Mike Tang, Milan Dimic, Rashmi Pai, Robert Saliba, Sahil Anguralla, Salik Chodhary, Sandhya Sainath, Scott Cederberg, Shorya Jain, Shubham Gupta, Sreekanth Sivasankaran, Srinivas Vuyyuru, Yiyu Pan, Yuqi Zhang, Yuriy Bondaruk, Zhaokun Li, Zhewei Mai.
Cover Photo Attribution: Generated by Gemini
Search Architecture Diagram (Modified by Gemini)
Nimish Sheth
Distinguished Engineer
Nimish is a Distinguished Engineer at Uber. He’s been at Uber for 10+ years across 2 stints. He helped architect Uber’s Payments Platform from the ground up. More recently, he’s been working on Uber Eats, specifically focusing on Search and B2B platforms.
Daniel Cai
Staff Software Engineer, TLM
Daniel is a Staff Tech Lead Manager at Uber with over six years of experience building search and discovery products. He has helped develop Uber Eats Search, focusing on search retrieval, relevance, and user experience at scale.
Saurabh Kathpalia
Staff Software Engineer
Saurabh is a Staff Software Engineer at Uber. He has been at Uber for 8 years. He helped architect Delivery Search Ingestion from the ground up, scaling it to support billions of catalog items. More recently, he's been leveraging GenAI to drive Search latency and efficiency optimizations.
Vishnu Akhilesh Venkataraman
Sr Software Engineer
Vishnu is a Senior Software Engineer at Uber, where he works on building search systems at scale. Across more than six years at Uber, he has contributed to systems spanning infrastructure, pricing, incentives, and currently, search.
Colin Schoen
Staff Software Engineer
Colin Schoen is a Staff Software Engineer who has spent five years at Uber designing feed and search systems for Uber Eats. He focuses on presentation architecture and frameworks that scale both in traffic and in the number of engineers building on them.
