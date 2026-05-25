# Day 1: Transformers Basics

## 1. What is it?
- **Simple Explanation:** Transformers are the foundational "brain" architecture behind all modern AI models like ChatGPT, Claude, Gemini, and Midjourney. Instead of reading text word-by-word like older AIs, Transformers process the entire text sequence at once, letting them see the "big picture" instantly.
- **One-line Definition:** A deep learning architecture based entirely on the **Attention mechanism** that processes input sequences in parallel and maps dependencies between all elements in a single step.
- **Why it exists:** Before Transformers, we used Recurrent Neural Networks (RNNs, LSTMs). These processed words sequentially (one-by-one). This meant:
  1. They were incredibly slow and couldn't scale on modern GPU hardware.
  2. They suffered from the "vanishing gradient" problem, meaning they "forgot" words at the beginning of long sentences.
- **What problem it solves:** 
  - **Sequential Training Bottleneck:** Allows massive parallelization during training, enabling us to train models on trillions of tokens.
  - **Memory Loss (Long-Range Dependencies):** Allows models to accurately associate words that are thousands of tokens apart in a text.

---

## 2. Core Intuition
- **Real-World Analogy (The Spotlight):**
  Imagine you are reading a complex legal contract. Your eyes don't pay equal attention to every single word. Instead, when you look at a word like **"Penalty"**, your eyes immediately "spotlight" and jump to other related words like **"Late"**, **"$500"**, or **"Termination"**. You use this spotlight network to construct the true meaning of the sentence. 
  - **Self-Attention** is this mathematical spotlight that tokens use to talk to and understand each other.
- **Simple Workflow:**
  ```text
  Raw Text ➔ Tokenization ➔ Embeddings ➔ Positional Encoding ➔ Attention Layers ➔ Linear/Softmax ➔ Next Token
  ```
- **Easy Intuition:**
  Words have different meanings in different contexts. For example, **"Bank"** in *"river bank"* vs. *"investment bank"*. Self-attention is the math that pulls information from *"river"* or *"investment"* to update the representation of *"bank"* so the model knows exactly what it means.

---

## 3. Internal Working
Below is the visual flow of how text goes from user input to the final generated output, and how the attention mechanism processes relationships.

### High-Level LLM Generation Pipeline (Decoder-Only Model)
```text
User Input Prompt: "The AI model"
       ↓
[TOKENIZER] 
  ↳ Splits text into sub-word tokens and maps them to numerical IDs.
  ↳ ["The", " AI", " model"] ➔ [464, 9152, 1642]
       ↓
[EMBEDDING LAYER]
  ↳ Converts token IDs into dense semantic vectors (e.g., 4096 dimensions).
       ↓
[POSITIONAL ENCODING]
  ↳ Adds a mathematical wave signal (like RoPE) to vectors to inject word position info.
       ↓
[TRANSFORMER DECODER BLOCKS] (Repeated N times, e.g., 32 layers)
  ├── 1. Masked Self-Attention: Tokens query and look at previous tokens' contexts.
  └── 2. MLP / Feed-Forward Network: Processes token representations individually to refine features.
       ↓
[LM HEAD & SOFTMAX]
  ↳ Linear layer projects vectors to vocabulary size. Softmax converts scores to probabilities.
  ↳ e.g., {" generates": 85%, " thinks": 5%, " runs": 2%, ...}
       ↓
[SAMPLING ENGINE] (Temperature, Top-P, Top-K)
  ↳ Selects the winning token: " generates"
       ↓
Output Text: "The AI model generates"
```

### The Self-Attention Mechanism (Visual Query-Key-Value Flow)
For the input phrase: **"Bank of the river"** (focusing on how the word **"Bank"** resolves its meaning):

```text
1. Linear Projection (For every token):
   Multiply input vector by learned Weight Matrices (W_Q, W_K, W_V) to get Q, K, and V:
   - Query (Q):  "What am I looking for?"      ➔ Q_bank
   - Key (K):    "What info do I contain?"      ➔ K_river, K_bank, K_of, K_the
   - Value (V):  "What is my actual content?"   ➔ V_river, V_bank, V_of, V_the

2. Calculate Attention Score (Similarity matrix):
   Measure how much "Query" of "Bank" matches the "Keys" of all other words.
   
   [Q_bank] • [K_bank]  ➔ Score: 1.2
   [Q_bank] • [K_of]    ➔ Score: 0.1
   [Q_bank] • [K_the]   ➔ Score: 0.1
   [Q_bank] • [K_river] ➔ Score: 8.5  <-- Huge match!

3. Scale & Softmax (Normalization):
   Divide scores by √d_k (dimension of keys) to prevent gradient issues, then apply Softmax to get percentages:
   
   Softmax Scores: [ "Bank": 10%, "of": 4%, "the": 4%, "river": 82% ]

4. Weighted Value Sum:
   Multiply percentages by the actual Value vectors (V) and add them up:
   
   Output Vector for "Bank" = (0.10 * V_bank) + (0.04 * V_of) + (0.04 * V_the) + (0.82 * V_river)
   
   Result: The output embedding for "Bank" now contains 82% of the meaning of "river"!
```

---

## 4. Key Concepts

### Tokens
- **Definition:** The fundamental blocks of text parsed by an LLM. It can be a whole word, part of a word (sub-word), or a single character.
- **Why Important:** LLMs cannot process letters or strings directly. Tokenization converts text into integer IDs, keeping vocabulary size manageable while handling spelling variations.
- **Real Usage:** Hugging Face `tokenizers` library. The sentence `"I love tokenization!"` might be split into `["I", " love", " token", "ization", "!"]`.
- **Interview-Important Point:** Word count does not equal token count (Rule of thumb: 100 words ≈ 133 tokens). Rare words, code snippets, numbers, or non-English characters are tokenized into many sub-word pieces, which increases generation costs and latency.

### Embeddings
- **Definition:** A mathematical representation of a token as a dense vector of numbers in a high-dimensional space (e.g., 4096 dimensions).
- **Why Important:** It maps semantic meaning into geometry. Words with similar meanings or contexts (like "King" and "Queen") sit closer together in this space.
- **Real Usage:** Creating document search indices in RAG pipelines using OpenAI's `text-embedding-3-small` or Hugging Face's `sentence-transformers`.
- **Interview-Important Point:** Input embeddings are static (look up table). They become contextual only *after* passing through the Self-Attention layers.

### Attention
- **Definition:** A mechanism that allows the model to compute weighted relationships between different elements in a sequence, dynamically focusing on what's important.
- **Why Important:** It allows the model to connect information across the entire input, bypassing the sequential bottleneck of RNNs.
- **Real Usage:** Image-to-text generators focusing on specific regions of an image when writing a caption.
- **Interview-Important Point:** Standard attention has a complexity of $O(N^2)$ (quadratic) with respect to sequence length. This makes processing long documents computationally expensive.

### Self-Attention
- **Definition:** A variation of attention where Query, Key, and Value vectors all originate from the same input sequence.
- **Why Important:** It enables tokens within a single sentence to interact, allowing each token to build context-sensitive meanings.
- **Real Usage:** Inside the Multi-Head Attention layer of models like Llama or GPT.
- **Interview-Important Point:** Causal Decoders use *Masked* Self-Attention. During training, it masks future tokens (sets attention weights to $-\infty$ for future tokens) to ensure the model only looks at past context when predicting the next word.

### Positional Encoding
- **Definition:** Extra vectors containing positional signals added to token embeddings to preserve the order of words.
- **Why Important:** Transformers process all tokens simultaneously, making them permutation-invariant (order-blind). Without positional encoding, `"Dog eats food"` and `"Food eats dog"` would look identical.
- **Real Usage:** Rotary Position Embeddings (RoPE) used in modern LLMs like Llama-3 and Mistral.
- **Interview-Important Point:** Traditional models used absolute position encodings (fixed sine/cosine values). Modern LLMs use relative encodings (like RoPE) because they generalize better to longer context lengths.

### Context Window
- **Definition:** The maximum number of tokens a model can process in a single API request/forward pass (includes both prompt and output).
- **Why Important:** Limits how much information (chat history, codebase files, PDFs) you can feed the model at once.
- **Real Usage:** Gemini 1.5 Pro features a 2-million token context window; Llama-3-8B has an 8k context window.
- **Interview-Important Point:** Doubling the context window size increases the size of the attention matrix by $4\times$, putting severe stress on GPU memory (specifically VRAM).

### Encoder vs. Decoder
- **Definition:** 
  - **Encoder (e.g., BERT):** Processes text bidirectionally (looks forward and backward).
  - **Decoder (e.g., GPT/Llama):** Processes text auto-regressively (looks only at past tokens).
  - **Encoder-Decoder (e.g., T5/BART):** Encoder reads input text, Decoder generates output text.
- **Why Important:** Dictates what tasks a model is good at.
- **Real Usage:** BERT is used for search ranking and classification. GPT is used for chatbots and generation. T5 is used for machine translation.
- **Interview-Important Point:** Encoders are bidirectional (uncausal). Decoders are causal (masked attention).

### Decoder-Only Models
- **Definition:** A Transformer architecture that drops the encoder entirely, using only causal decoder blocks to generate text token-by-token.
- **Why Important:** It is highly efficient for general text generation and displays behavior like "In-Context Learning" (zero-shot and few-shot prompting).
- **Real Usage:** Almost all modern LLMs (GPT-4, Llama, Claude, Mistral) are decoder-only.
- **Interview-Important Point:** Decoder-only models are easier to scale to hundreds of billions of parameters because the next-token prediction task is simple, consistent, and maps directly to generative inference.

### Hallucinations
- **Definition:** When an LLM generates text that is grammatically correct and confident, but factually incorrect or ungrounded.
- **Why Important:** The biggest roadblock to deploying LLMs in production systems (e.g., healthcare, finance).
- **Real Usage:** Guardrails (NeMo Guardrails, Llama Guard) and RAG are used in industry to prevent hallucinations.
- **Interview-Important Point:** Hallucination is not a bug; it is a direct consequence of how LLMs work. LLMs predict the *most probable* next token, not the *truest* next token. 

### Training vs. Inference
- **Definition:**
  - **Training:** Feeding data to a model, calculating loss, and updating model weights using backpropagation.
  - **Inference:** Loading a trained model with frozen weights to predict the next tokens on user prompts.
- **Why Important:** Dictates hardware choices. Training is compute-bound (requires high-bandwidth GPU clusters like H100s). Inference is memory-bandwidth bound (bottlenecked by how fast we can load weights from GPU memory to processor).
- **Real Usage:** Pre-training a model costs millions of dollars; running daily inference cost is the primary operational expense for companies.
- **Interview-Important Point:** During training, we use **Teacher Forcing** (masked attention lets us process all targets in parallel). During inference, we must run the model sequentially (auto-regressive), predicting one token at a time.

---

## 5. Practical Understanding (LLM Engineering in Production)

### How Companies Deploy & Optimize Transformers
1. **FlashAttention (1 & 2):** 
   - **What it is:** A hardware-friendly implementation of attention. Instead of calculating and writing the massive $N \times N$ attention matrix to slow High-Bandwidth Memory (HBM), it calculates it in chunks using GPU SRAM.
   - **Production Impact:** Reduces memory usage by up to $10\times$ and speeds up training/inference by $2-4\times$.
2. **KV Caching (Key-Value Cache):**
   - **The Problem:** During auto-regressive generation, to generate token 101, the model re-computes the Q, K, and V vectors for tokens 1 to 100. For token 102, it re-computes tokens 1 to 101. This is a massive waste of GPU cycles.
   - **The Solution:** We store the Keys and Values (KV Cache) of past tokens in GPU memory. For the next step, we only compute Q, K, and V for the *new* token.
   - **Production Impact:** Speeds up generation latency from $O(N^2)$ to $O(N)$ (linear).
3. **Quantization:**
   - **What it is:** Reducing the precision of the model weights (e.g., from FP16 to INT8 or INT4).
   - **Production Impact:** Allows a model that originally required 16GB of VRAM (FP16) to run on a cheaper 4GB GPU (INT4) with minimal quality loss.
4. **Continuous Batching:**
   - **What it is:** Traditional batching waits for a batch of 8 users to finish generating text. Continuous batching schedules requests at the *iteration* level. As soon as one user's prompt is done, a new user's request is swapped in.
   - **Production Impact:** Boosts throughput of serving engines (like **vLLM**) by up to $10\times$.

---

## 6. Code Example (Modern Production-Ready Inference)

To avoid gated-model token requirements (like Llama-3), we use the popular open-weight model **Qwen/Qwen2.5-0.5B-Instruct**. This script demonstrates loading, initializing, and generating text with modern best practices.

```python
# Install command: pip install transformers accelerate torch
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# 1. Define model ID (using a high-quality, open-access lightweight model)
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def main():
    print(f"Loading tokenizer for {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # BEST PRACTICE: For auto-regressive decoders, set pad token to eos token
    # and pad on the LEFT. Left padding ensures the attention masks align 
    # correctly during batch generation.
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    print(f"Loading model weights into memory...")
    # BEST PRACTICE: 
    # - torch_dtype=torch.bfloat16: Uses 16-bit brain float to save 50% VRAM over FP32
    # - device_map="auto": Automatically loads layers onto GPU if available, else CPU
    # - low_cpu_mem_usage=True: Optimizes memory overhead during model load
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )

    # 2. Build pipeline (highly optimized abstraction)
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )

    # 3. Create instruction-tuned prompt structure
    # Modern models perform best when prompts are wrapped in a structured template
    messages = [
        {"role": "system", "content": "You are a helpful and concise AI assistant."},
        {"role": "user", "content": "Explain the concept of 'Attention' in one sentence."}
    ]
    
    # Format message list to raw tokenized text format
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )

    print("\n--- Generating Response ---")
    # BEST PRACTICE Sampling Parameters:
    # - do_sample=True: Enables probabilistic token selection
    # - temperature=0.7: Controls randomness (lower = more deterministic)
    # - top_p=0.9: Nucleus sampling (ignores low-probability tails)
    # - max_new_tokens=100: Hard limit on generation length to control VRAM & latency
    outputs = generator(
        prompt,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

    # Extract and display output text
    generated_text = outputs[0]["generated_text"]
    
    # Strip the prompt to display only the model's response
    response_only = generated_text[len(prompt):]
    
    print("\nPrompt Sent to Model:")
    print(prompt)
    print("\nModel Output:")
    print(response_only.strip())

if __name__ == "__main__":
    main()
```

---

## 7. Common Interview Questions

### Beginner Questions

#### Q1: What is a Token and how does it differ from a Word?
- **Short Answer:** A token is the basic unit of text an LLM reads (can be characters, subwords, or words). A word is a complete unit of human language.
- **Industry Perspective:** In production, pricing and speed are measured in tokens. A word like "understanding" might be 1 token, but "und3rst4nd1ng" will be tokenized into 5+ tokens, making it slower and more expensive to process.

#### Q2: Why is the scale factor $\sqrt{d_k}$ used in Dot-Product Attention?
- **Short Answer:** As the dimension of the keys $d_k$ grows large, the dot products grow large in magnitude. This pushes the softmax function into regions with extremely small gradients (vanishing gradient). Dividing by $\sqrt{d_k}$ counteracts this scaling effect.
- **Industry Perspective:** Without this scaling factor, training models with large hidden dimensions (e.g., 4096+) would fail to converge.

#### Q3: What is the purpose of Positional Encoding?
- **Short Answer:** Self-attention processes tokens in parallel, losing sequence order. Positional encoding adds position-related values to embeddings so the model knows word order.
- **Industry Perspective:** Choosing the right positional encoding (like RoPE) directly affects how far a model can extrapolate context in production.

---

### Medium Questions

#### Q1: Explain the Key-Value (KV) Cache and its trade-offs.
- **Short Answer:** The KV cache stores the Key and Value activations of past tokens in memory during inference, preventing recomputations.
- **Industry Perspective:** The primary trade-off is **speed vs. memory**. While it makes generation significantly faster, the KV cache consumes massive VRAM. In high-concurrency production servers, KV cache memory limits maximum batch size, prompting the use of memory-saving variants like Multi-Query Attention (MQA) or Grouped-Query Attention (GQA).

#### Q2: What is the difference between causal masking and bidirectional masking?
- **Short Answer:** Causal masking prevents a token from attending to future tokens (used in Decoders for text generation). Bidirectional masking allows a token to attend to all tokens in the sequence (used in Encoders for understanding).
- **Industry Perspective:** Decoders must use causal masking to mimic auto-regressive generation; otherwise, they would "cheat" during training by looking at the future words they are supposed to predict.

#### Q3: What are Multi-Head Attention (MHA), Multi-Query Attention (MQA), and Grouped-Query Attention (GQA)?
- **Short Answer:** 
  - **MHA:** Each head has unique Query, Key, and Value projections.
  - **MQA:** All heads share a single Key and Value projection, but have unique Query projections.
  - **GQA:** Heads are grouped; each group shares a single Key and Value projection.
- **Industry Perspective:** MQA and GQA reduce KV cache size drastically (up to $8\times$), allowing for larger batch sizes and higher throughput in production inference servers. Llama-3 uses GQA.

---

### Advanced Questions

#### Q1: Explain Rotary Position Embedding (RoPE) and why it's better than Sinusoidal Positional Encoding.
- **Short Answer:** RoPE applies a rotation matrix to Query and Key vectors in 2D pairs. It encodes *relative* distance between tokens rather than *absolute* index positions.
- **Industry Perspective:** Because RoPE encodes relative distance, we can dynamically scale it (via Interpolation) to extend context windows (e.g., from 8k to 128k) during inference without retraining the model from scratch.

#### Q2: How do you estimate the GPU VRAM required to load an 8-Billion parameter model for inference?
- **Short Answer:** 
  - In FP16 precision: $\text{Params} \times 2 \text{ bytes} = 8 \times 2 = 16\text{ GB}$.
  - In INT8 (8-bit quantization): $\text{Params} \times 1 \text{ byte} = 8\text{ GB}$.
  - In INT4 (4-bit quantization): $\text{Params} \times 0.5 \text{ bytes} = 4\text{ GB}$.
  - Add $\sim 20-30\%$ overhead for KV cache, system kernels, and activation memory.
- **Industry Perspective:** Knowing this math is critical for capacity planning. To serve Llama-3-8B in FP16, you need at least a 24GB GPU (like an A10G or L4). In INT4, it can comfortably fit on a cheaper 8GB consumer GPU.

#### Q3: Contrast the Prefill phase vs. Decoding phase in LLM inference.
- **Short Answer:** 
  - **Prefill phase:** Processes the input prompt. It runs in parallel, utilizes GPU compute fully, and is **compute-bound**.
  - **Decoding phase:** Generates output tokens one-by-one. It runs sequentially, requires reloading model weights for every single token, and is highly **memory-bandwidth bound**.
- **Industry Perspective:** Serving engines optimize these separately (e.g., chunked prefills) to balance Time to First Token (TTFT) and Inter-Token Latency (ITL).

---

## 8. Important Comparisons

### Encoder (BERT) vs. Decoder (GPT)
| Feature | Encoder (e.g., BERT) | Decoder (e.g., GPT / Llama) |
| :--- | :--- | :--- |
| **Attention Mask** | Bidirectional (Looks left & right) | Causal (Looks left only) |
| **Task Fit** | Classification, NER, Embeddings | Text generation, Chat, Code |
| **Inference** | Single forward pass | Sequential/Auto-regressive |
| **Training Task** | Masked Language Modeling (fill-in-the-blank) | Causal Language Modeling (predict next word) |

### Standard Attention vs. FlashAttention
| Feature | Standard Attention | FlashAttention |
| :--- | :--- | :--- |
| **Memory Read/Write** | High (Writes $N \times N$ matrix to GPU HBM) | Low (Keeps intermediate matrix in SRAM) |
| **Time Complexity** | $O(N^2)$ | $O(N^2)$ (Same math, faster execution) |
| **Memory Complexity**| $O(N^2)$ | $O(N)$ (Linear memory footprint) |
| **Hardware Speedup** | Baseline | $2\times$ to $4\times$ faster |

---

## 9. Common Mistakes

### 1. Beginner Mistakes
- **Incorrect Padding Side:** Padding on the right during batch generation. In Decoders, right padding puts pad tokens at the end, messing up the model's causal attention alignment. Always use **left padding** for generation.
- **Confusing Character/Word Count with Tokens:** Building logic assuming 1 word = 1 token. This causes unexpected prompt truncation or out-of-memory errors when handling dense, multilingual, or special symbols.

### 2. Production Mistakes
- **Running Inference Without KV Caching:** Disabling or forgetting to pass the past key values. This turns an $O(N)$ inference process into $O(N^2)$, making the response time slow down exponentially as the generation gets longer.
- **Underestimating VRAM Overhead:** Budgeting only for model weights. The KV Cache grows dynamically with user request length and batch size. Under-provisioning VRAM leads to frequent Out-Of-Memory (OOM) crashes in production.

### 3. Performance Mistakes
- **Running Inference in FP32:** Using default 32-bit floats. This consumes double the VRAM and misses out on GPU tensor core acceleration. Always run LLM inference in **FP16 or BF16**.
- **Using a Decoder-only LLM for Basic Embeddings:** Running Llama-3-8B to generate embeddings for similarity search. A small bidirectional Encoder model (like `all-MiniLM-L6-v2`) is $100\times$ faster, uses a fraction of the VRAM, and yields higher-quality sentence embeddings.

---

## 10. Quick Revision Notes

### Formula Cheat Sheet
- **Scaled Dot-Product Attention:** 
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
- **FP16 Model VRAM Requirement:** 
  $$\text{VRAM (GB)} \approx \text{Parameters (Billion)} \times 2$$

### 10 Fast-Revision Points
1. **Transformers** replaced RNNs due to parallel training capability and long-range memory.
2. **Tokens** are the vocabulary building blocks. 100 words $\approx$ 133 tokens.
3. **Embeddings** represent words in high-dimensional vector space, mapping semantic meanings.
4. **Self-Attention** maps semantic dependencies by allowing tokens to compute weight matrices with every other token in the sequence.
5. **Positional Encoding** adds order information. Modern models use relative **RoPE (Rotary)** encoding.
6. **Decoders** use **Causal Masking** to block future tokens during training and generation.
7. **KV Caching** prevents recomputations of Keys and Values, speeding up sequential text generation.
8. **FlashAttention** accelerates attention computation by keeping computations in fast GPU SRAM.
9. **Prefill** (prompt processing) is compute-bound, whereas **Decoding** (token generation) is memory-bandwidth bound.
10. **Left Padding** is mandatory for batch generation inside Decoder models.
