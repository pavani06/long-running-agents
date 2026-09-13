---
url: "https://arxiv.org/abs/2511.08567"
key: "dc8e284c3c3c"
status: "ok"
final_url: "https://arxiv.org/abs/2511.08567"
method: "trafilatura"
content_hash: "8ad03b4cdc95fbde4931cce0fa37f138ef397a1d"
text_len: 3604
fetched: "2026-09-13"
---

Computer Science > Machine Learning
  [Submitted on 11 Nov 2025]
    Title:The Path Not Taken: RLVR Provably Learns Off the Principals
View PDF HTML (experimental)
            Abstract:Reinforcement Learning with Verifiable Rewards (RLVR) reliably improves the reasoning performance of large language models, yet it appears to modify only a small fraction of parameters. We revisit this paradox and show that sparsity is a surface artifact of a model-conditioned optimization bias: for a fixed pretrained model, updates consistently localize to preferred parameter regions, highly consistent across runs and largely invariant to datasets and RL recipes. We mechanistically explain these dynamics with a Three-Gate Theory: Gate I (KL Anchor) imposes a KL-constrained update; Gate II (Model Geometry) steers the step off principal directions into low-curvature, spectrum-preserving subspaces; and Gate III (Precision) hides micro-updates in non-preferred regions, making the off-principal bias appear as sparsity. We then validate this theory and, for the first time, provide a parameter-level characterization of RLVR's learning dynamics: RLVR learns off principal directions in weight space, achieving gains via minimal spectral drift, reduced principal-subspace rotation, and off-principal update alignment. In contrast, SFT targets principal weights, distorts the spectrum, and even lags RLVR.
Together, these results provide the first parameter-space account of RLVR's training dynamics, revealing clear regularities in how parameters evolve. Crucially, we show that RL operates in a distinct optimization regime from SFT, so directly adapting SFT-era parameter-efficient fine-tuning (PEFT) methods can be flawed, as evidenced by our case studies on advanced sparse fine-tuning and LoRA variants. We hope this work charts a path toward a white-box understanding of RLVR and the design of geometry-aware, RLVR-native learning algorithms, rather than repurposed SFT-era heuristics.
References & Citations
    
    Loading...
Bibliographic and Citation Tools
            Bibliographic Explorer (What is the Explorer?)
          
        
            Connected Papers (What is Connected Papers?)
          
        
            Litmaps (What is Litmaps?)
          
        
            scite Smart Citations (What are Smart Citations?)
          
        Code, Data and Media Associated with this Article
            alphaXiv (What is alphaXiv?)
          
        
            CatalyzeX Code Finder for Papers (What is CatalyzeX?)
          
        
            DagsHub (What is DagsHub?)
          
        
            Gotit.pub (What is GotitPub?)
          
        
            Hugging Face (What is Huggingface?)
          
        
            ScienceCast (What is ScienceCast?)
          
        Demos
Recommenders and Search Tools
              Influence Flower (What are Influence Flowers?)
            
          
              CORE Recommender (What is CORE?)
            
          
              IArxiv Recommender
              (What is IArxiv?)
            
          arXivLabs: experimental projects with community collaborators
arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.
Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.
Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.
