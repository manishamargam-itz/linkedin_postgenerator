from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, use_emojis=True):
    prompt = get_prompt(length, language, tag, use_emojis)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, use_emojis):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a professional LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    4) Style: Professional, engaging, and authentic
    {f"5) Add relevant emojis to make the post more engaging" if use_emojis else "5) Do not use any emojis"}
    
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    
    The post should:
    - Start with an attention-grabbing hook
    - Include personal insights or experiences
    - End with a call to action or thought-provoking question
    - Be formatted with proper spacing and line breaks
    '''

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\n\n6) Use the writing style as per the following examples:"

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))