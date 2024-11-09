import groq
import time
import os
import json

def make_api_call(messages, max_tokens, is_final_answer=False, custom_client=None):
    if custom_client != None:
        client = custom_client
    
    for attempt in range(3):
        try:
            if is_final_answer:
                response = client.chat.completions.create(
                    model="gemma2-9b-it",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.2,
            ) 
                return response.choices[0].message.content
            else:
                response = client.chat.completions.create(
                    model="gemma2-9b-it",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
        except Exception as e:
            if attempt == 2:
                if is_final_answer:
                    return {"title": "Error", "content": f"Failed to generate final answer after 3 attempts. Error: {str(e)}"}
                else:
                    return {"title": "Error", "content": f"Failed to generate step after 3 attempts. Error: {str(e)}", "next_action": "final_answer"}
            time.sleep(1)  

def generate_response(prompt, custom_client=None):
    messages = [
        {"role": "system", "content": """You are an expert AI assistant tasked with evaluating the completeness and thoroughness of a review. Your goal is to classify reviews as either 'Exhaustive' or 'Trivial' based on their coverage of key sections and aspects. Here are the definitions of the terms:

1. **Exhaustive**: The review provides comprehensive feedback across multiple sections and aspects of the paper, offering detailed insight into key areas such as methodology, results, experiments, and more. A review should be classified as 'Exhaustive' if it covers a wide range of sections and aspects (e.g., Abstract, Introduction, Methodology, etc.) with depth, leaving no significant sections or questions unaddressed.

2. **Trivial**: The review lacks depth and does not sufficiently cover critical sections or aspects. It might focus only on one or two areas (e.g., comments on Abstract or Introduction) and fails to address significant sections or aspects in detail. A 'Trivial' review might provide shallow or vague comments that do not contribute much to improving the paper.

Here are the key sections and aspects you should be aware of:
Sections: Abstract (ABS), Introduction (INT), Related Works (RWK), Problem Definition/Idea (PDI), Data/Datasets (DAT), Methodology (MET), Experiments (EXP), Results (RES), Tables & Figures (TNF), Analysis (ANA), Future Work (FWK), Overall (OAL), Bibliography (BIB), External Knowledge (EXT).
Aspects: Appropriateness (APR), Originality/Novelty (NOV), Significance/Impact (IMP), Meaningful Comparison (CMP), Presentation/Formatting (PNF), Recommendation (REC), Empirical/Theoretical Soundness (EMP), Substance (SUB), Clarity (CLA).

For example, a review that comments on several sections like 'Methodology,' 'Experiments,' and 'Results' in detail and provides constructive feedback on 'Originality,' 'Significance,' and 'Empirical Soundness' should be considered exhaustive. A review that only comments on the 'Introduction' or 'Abstract' without providing much insight into other sections should be considered trivial.

### Important:
**Your decision MUST be directly supported by the step-by-step reasoning in the CoT (Chain of Thought).** Carefully evaluate each section and aspect mentioned in the CoT reasoning before making your final decision.

### Double-Check:
Before you finalize your decision, ask yourself: 'Does the reasoning I've provided support an 'Exhaustive' or 'Trivial' decision?' Your decision **must align** with the CoT reasoning.

For each step in your reasoning, provide a title that describes what you're examining in that step, along with detailed content. Decide if you need another step or if you're ready to give the final classification. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer') keys.

Example of a valid JSON response:
```json
{
    "title": "Identifying Key Sections Covered",
    "content": "First, let's examine which sections of the paper this review addresses. The review discusses...",
    "next_action": "continue"
}```"""},
        {"role": "user", "content": f"{prompt}\n\nEvaluate the review's coverage of sections and aspects based on the reasoning provided. Please make sure the reasoning strictly follows **Chain of Thought (CoT)** steps."},
        {"role": "assistant", "content": "I will now analyze this review step by step, examining its coverage of sections and aspects to determine if it's 'Exhaustive' or 'Trivial'."}
    ]
    
    steps = []
    step_count = 1
    total_thinking_time = 0
    
    while True:
        start_time = time.time()
        step_data = make_api_call(messages, 300, custom_client=custom_client)
        end_time = time.time()
        thinking_time = end_time - start_time
        total_thinking_time += thinking_time
        
        steps.append((f"Step {step_count}: {step_data['title']}", step_data['content'], thinking_time))
        
        messages.append({"role": "assistant", "content": json.dumps(step_data)})
        
        if step_data['next_action'] == 'final_answer' or step_count > 25: 
            break
        
        step_count += 1

        yield steps, None  
    
    messages.append({"role": "user", "content": "Based on your step-by-step analysis above, provide your final classification of the review as either 'Exhaustive' or 'Trivial'. Explain why this classification aligns with your CoT reasoning."})
    
    start_time = time.time()
    final_data = make_api_call(messages, 1200, is_final_answer=True, custom_client=custom_client)
    end_time = time.time()
    thinking_time = end_time - start_time
    total_thinking_time += thinking_time
    
    steps.append(("Final Answer", final_data, thinking_time))

    yield steps, total_thinking_time