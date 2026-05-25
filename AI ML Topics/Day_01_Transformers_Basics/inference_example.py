# Installation: pip install transformers accelerate torch
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Using a high-quality, open-access, lightweight instruct model.
# This prevents gated token errors (e.g. from meta-llama/Llama-3 models)
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def run_inference():
    print(f"Loading tokenizer for: {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # BEST PRACTICE: Set padding token to EOS token for generative decoder models
    # Set padding_side to 'left' as it is required for batch generation to keep positional IDs consistent
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    print(f"Loading model: {MODEL_ID}...")
    # BEST PRACTICE: 
    # - device_map="auto": Automatically targets CUDA GPU(s) if available, otherwise falls back to CPU
    # - torch_dtype=torch.bfloat16: Cuts memory usage by 50% compared to FP32 while maintaining numerical stability
    # - low_cpu_mem_usage=True: Optimizes memory usage during initial layer loading
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto", 
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )

    # 3. Build text-generation pipeline
    # The pipeline handles tokenization, forward pass, and generation sampling internally
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    # 4. Formulate the input using chat templates (Standardized Instruct Format)
    messages = [
        {"role": "system", "content": "You are a helpful and concise AI assistant."},
        {"role": "user", "content": "Explain the core concept of Attention in one sentence:"}
    ]
    
    # Apply Chat Template transforms structured messages to the raw format the model was trained on
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )
    
    print("\n" + "=" * 40)
    print(f"PROMPT PASSED TO MODEL:\n{prompt}")
    print("=" * 40 + "\n")

    # 5. Generate text with modern sampling settings
    # - max_new_tokens: Caps output size to control latency and prevent run-away generations
    # - do_sample: Enables probabilistic sampling (required for temperature/top_p)
    # - temperature: Controls output diversity (0.7 is a good balance of creativity and structure)
    # - top_p: Nucleus sampling (cuts off the least likely tokens to avoid nonsense)
    output = generator(
        prompt,
        max_new_tokens=80,
        do_sample=True,      
        temperature=0.7,    
        top_p=0.9,          
        pad_token_id=tokenizer.eos_token_id
    )

    # 6. Extract response
    full_output = output[0]['generated_text']
    response_only = full_output[len(prompt):].strip()

    print("=" * 40)
    print("GENERATED RESPONSE:")
    print(response_only)
    print("=" * 40)

if __name__ == "__main__":
    run_inference()
