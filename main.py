from fastapi import FastAPI, Request
import traceback
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

@app.post("/agent")
async def agent_endpoint(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message", "")

        if not user_message:
            return {"error": "No se recibió mensaje."}

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un agente de ventas especializado en productos de tecnología, gestionas inventarios, ofreces siempre el producto más nuevo, propones alternativas económicas justificando ventajas, y actualizas inventario vía enlaces web si el administrador usa la clave admstock33."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        agent_reply = response.choices[0].message.content
        return {"response": agent_reply}

    except Exception as e:
        print("❌ ERROR EN EL SERVIDOR:")
        traceback.print_exc()
        return {"error": "Falla interna al consultar el agente."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)