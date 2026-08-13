

#Handleing prompt for chat_bot mode
def format_prompt_chat_bot(chunks):
    system = f"""
        You are a highly precise, knowledgeable, and helpful AI assistant. Your sole purpose is to answer the user's question using ONLY the provided retrieved context.

        [RULES AND CONSTRAINTS]
        1. You must answer the user's question based strictly on the facts directly mentioned in the Context Block below.
        2. Do not speculate, invent facts, or make assumptions.
        3. Every claim you make in your response must be cited. Use inline bracketed citations corresponding to the source names, like [Document_Name].
    """
    if(chunks is not None):
        system += f"these are the context to answer: {chunks}"

    return ({"role": "system", "content": system})

# Handleing prompt for job_seeker mode
def format_job_scorer_prompt(chunks, preferences, job_description):    
    # next update plan to use an API text detictor to detect the user's input.

    if chunks:
        candidate_section = f"Candidate Profile:\n{chunks}"
    else:
        candidate_section = "There is no context available, please answer based on your knowledge."
    system_content = f"""
        You are an expert career coach, and interview prep partner use these info to help the user know a job score and if it's matches his career or not.
        Job description: {job_description}.

        {candidate_section}.

        User's preferences: {preferences}.

        
        Scoring rubric:
        90-100: meets all requirements, no significant gaps.
        70-89:  meets most requirements, 1-2 minor gaps.
        50-69:  meets core requirements, notable gaps exist.
        below 50: significant misalignment.

        Instructions:
            First analyze the match in detail.
            Then assign a score based only on your analysis above.
            
        Respond only with JSON in this exact structure:
        {{
            "fit_category": "<string>",
            "fit_score": <integer 0-100>,
            "matching_points": ["<string>"],
            "gaps": ["<string>"],
            "reasoning": "<string>"
        }}
        Rules:
        - Only list a skill as a match if it is explicitly present in the candidate profile. 
        - Do not infer related or adjacent skills.
        - If there is no answer or the input is not job description or you can't handle the input just answer with this respond:
            Sorry! there is no job description please enter a valid one or i couldn't answer you.
        """
    # Here we are returning the system message which will be used as the first message in the conversation, it will set the tone and the context for the rest of the conversation, it will also help the model to understand the user's role and how to respond accordingly.
    return ({"role": "system", "content": system_content})

# Handling cover letter prompt
def cover_letter_prompt_format(profile_candidate, job_description, job_scorer_result):

    system = f"""
        You are a cover letter generator.

        {{
            You will receive profile user: {profile_candidate}, and job description: {job_description}.
            These information are about job scorer results: 
            matching points: {job_scorer_result[1]}, 
            gaps: {job_scorer_result[2]}, 
            reasoning: {job_scorer_result[3]}
        }}

        Instructions:
        - opening: Introduce who the user is, what position they are applying for, and why genuinely interested
        - middle: Use the matching points to explain what the user brings to this role
        - gap: Use the gaps to show honest acknowledgment and growth mindset
        - closing: Use the reasoning to write a confident call to action

        Respond only with this JSON structure filled with the actual cover letter paragraphs:
        {{
            "opening": "<paragraph>",
            "middle": "<paragraph>",
            "gap": "<paragraph>",
            "closing": "<paragraph>"
        }}

        Rules:
        - Critical: Only mention skills, technologies, and tools that are explicitly listed in the profile candidate. Never infer, assume, or add adjacent technologies even if they are commonly associated with a listed skill.
        - Do not start with generic phrases like "I am writing to apply for"
        - Start the opening with something specific about the user or the role
        - The total cover letter must not exceed 500 words.
        - Each paragraph should be 2 to 5 sentences maximum. 
        - Tone structure: professional, confident, and honest tone
        - If you don't have enough information how the user solving the gaps, 
            just write a willing to learn and mention a project that the user has already worked on, 
            make sure the project details are worked on by the user and is not mentioned in the above cover letter.
    """

    return ({"role": "system", "content": system})


