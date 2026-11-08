from pydantic import BaseModel,Field

class RagQuestion(BaseModel):
    question: str = Field(min_length=1,max_length=1000)

class RagAnswer(BaseModel):
    answer:str
    citations:list[dict]

class DocumentIndexRequest(BaseModel):
    file_name: str =Field(min_length=1,max_length=255)
