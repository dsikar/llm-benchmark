#!/usr/bin/env python3

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def main():
    model_name = "microsoft/DialoGPT-medium"
    prompt = "Explain the concept of vanishing gradients"
    
    print(f"Loading model: {model_name}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        print(f"Model loaded successfully")
        print(f"Using device: {next(model.parameters()).device}")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = inputs.to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 150,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response[len(prompt):].strip()
        
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())