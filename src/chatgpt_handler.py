import openai

def generate_response(system_prompt, user_input, history=None, model="gpt-4", api_key=None):
    client = openai.OpenAI(api_key=api_key)
    messages = [{"role": "system", "content": system_prompt}]
    
    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip()

def generate_idle_thoughts(personality, count, api_key, model="gpt-4"):
    system_prompt = f"You are a {personality}. You express yourself with short, quirky internal thoughts."
    prompt = f"Give me {count} short, funny internal thoughts that this character might think randomly to themselves. List them."

    result = generate_response(system_prompt, prompt, model=model, api_key=api_key)

    # Parse and clean list of thoughts
    thoughts = [line.lstrip("-•0123456789. ").strip() for line in result.splitlines() if line.strip()]
    return thoughts
