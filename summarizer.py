import openai

def summarize_results(generated_prompt, company_name, financials=None):
    if financials is not None:
        prompt = (
            "You know the following context information."
            f"{generated_prompt}"
            f"And an attached financtial values {financials}"
            "Question:" 
            "Using the retrieved result first combined with internet result, create an investment memo that captures all of the following header:" 
            "Product/Services Overview:\n\n"
            "Value Proposition:\n\n"
            "Customer Segment:\n\n"
            "Revenue Model:\n\n"
            "Number of Employee and Department:\n\n"
            "The Key Management Teams, Their Background and Roles:\n\n"
            "Market Overview:\n\n"
            "Investment Thesis:\n\n"
            "and Risk:\n\n"
        )
    else:
        prompt = (
            f"""You know the following context information for the company {company_name}: 
            
            {generated_prompt}
            
            Question: 
            Using the context information, generate an investment memo. Do not dispaly any information outside of 
            the context information. Generated response should be in a well structured format and easy to read and understand.
            Include all numbers and financial data and analyze them from the context information.
            
            Response:
            """
        )

    # Call the GPT model for summarization
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful experts that creates investment memo."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the summary
    summary = response['choices'][0]['message']['content']
    return summary
