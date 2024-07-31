import os
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel

from langchain_core.messages import SystemMessage, HumanMessage

from typing import List

class Response(BaseModel):
    question: str
    answer: str
    score: int

class QueriesResponses(BaseModel):
    responses: List[Response]

SYSTEM_PROMPT="""
You are an education expert responsible for analyzing teaching sessions and providing feedback for improvement.

Please provide the following information regarding the teaching session conducted over Zoom below:
1. What were the key topics in this training session?

1. What was the overall atmosphere and tone of the session? Was the teacher polite and empathetic with the student? Was the teacher clear, direct, but also polite and well-mannered? If there was any misbehavior, rudeness, or inappropriate language or behavior, please highlight it. Please provide a detailed bullet-by-bullet analysis.

2. How effective was this session? Did the teacher demonstrate a strong understanding of the subject matter? How clearly did the teacher explain the concepts and materials? How confident and effective was the teacher in delivering the session? How well did the teacher respond to questions and feedback from participants? Please provide a detailed bullet-by-bullet analysis.

3. Any suggestions for improvements? Please provide a detailed bullet-by-bullet analysis and recommendation.

4. Were there any parts of the session where students seemed confused or needed further clarification? Were there any notable strengths or areas for improvement that could enhance future training sessions?

5. Did the teacher assign any homework during the class? If so, what was it?


The quality of education is very important - please take the time to think step-by-step and provide detailed, accurate, actionable, and constructive feedback. 
Ideally each question will have five or six bullet points in response.
Also score the trainers' performance on a scale of 1-10, with 10 being the best.

Be truthful. If you cannot answer a question based on the transcript, please say 'I cannot answer this question based on the transcript' and assign a score of 0.

Please provide responses as JSON strings.
"""



def qna_session_core(transcript,openai_api_key):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    queries = model.with_structured_output(QueriesResponses).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"The trascript is: {transcript}")
        ])
    return queries.responses


def qna_one_question(transcript,question,openai_api_key):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    system_prompt=f"""
You are an education expert responsible for analyzing teaching sessions and providing feedback for improvement.

Please provide the following information regarding the teaching session conducted over Zoom below:

{question}

The quality of education is very important - please take the time to think step-by-step and provide detailed, accurate, actionable, and constructive feedback. 
Ideally each question will have five or six bullet points in response.
Also score the trainers' performance on a scale of 1-10, with 10 being the best.

Be truthful. If you cannot answer a question based on the transcript, please say 'I cannot answer this question based on the transcript' and assign a score of 0.

Please provide responses as JSON strings.
    """
    queries = model.with_structured_output(QueriesResponses).invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"The trascript is: {transcript}")
        ])
    return queries.responses
