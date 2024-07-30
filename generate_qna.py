import os
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel

from langchain_core.messages import SystemMessage, HumanMessage

from typing import List

class Response(BaseModel):
    question: str
    answer: str

class QueriesResponses(BaseModel):
    responses: List[Response]

SYSTEM_PROMPT="""
You are an education expert responsible for analyzing teaching sessions and providing feedback for improvement.

Please provide the following information regarding the teaching session conducted over Zoom below:
1. Was the teacher polite and empathetic with the student? Please provide a detailed bullet-by-bullet analysis.
2. How effective was this session? Please provide a detailed bullet-by-bullet analysis.
3. Any suggestions for improvements? Please provide a detailed bullet-by-bullet analysis and recommendation.
4. Did the teacher assign any homework during the class? If so, what was it?
5. Was the teacher clear, direct, but also polite and well-mannered in the class?
6. Was there any misbehavior, rudeness, or inappropriate language or behavior during the class? If so, what was it?
7. How clearly did the trainer explain the concepts and materials?
8. Were there any parts of the session where participants seemed confused or needed further clarification?
9. How well did the trainer respond to questions and feedback from participants?
10. Did the trainer demonstrate a strong understanding of the subject matter?
11. How clearly did the trainer explain the concepts and materials?
12. How confident and effective was the trainer in delivering the session?
13. What was the overall atmosphere and tone of the session?
14. Were there any notable strengths or areas for improvement that could enhance future training sessions?

The quality of education is very important - please take the time to think step-by-step and provide detailed, accurate, actionable, and constructive feedback. Ideally each question will have three bullet points in response.

Please provide responses as JSON strings.
"""



def qna_session_core(transcript,openai_api_key):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    queries = model.with_structured_output(QueriesResponses).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=transcript)
        ])
    return queries.responses
