AI Idea Factory is a project with simple input where the user can input a text and the API will return 5 blog post ideas. It is useful for bloggers and social media users to generate different blog post ideas based on specific niche.

https://github.com/user-attachments/assets/317ee9a1-6d86-43e2-a98b-b8adb02c7b05

# Installation
- Clone the project
- Run ```uvicorn main:app --reload```
- Open http://127.0.0.1:8000/ on your favourite browser


## Example request:
**POST** /generate-ideas
```
{
    "topic": "health"
}
```


