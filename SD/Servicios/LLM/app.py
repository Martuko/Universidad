from fastapi import FastAPI
import httpx, os, time

# Variables de entorno
OLLAMA = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL  = os.getenv("LLM_MODEL", "llama3.1:70b-instruct-q4_K_M")
MAX_TOK = int(os.getenv("LLM_MAX_TOKENS", "512"))
TEMP    = float(os.getenv("LLM_TEMPERATURE", "0.2"))

SYS_PROMPT = (
    "Eres un asistente conciso y factual. Responde en español y cita si corresponde."
)

app = FastAPI()

@app.post("/generate")
async def generate(payload: dict):
    """
    Endpoint principal: recibe una pregunta y devuelve respuesta del LLM.
    """
    question = payload.get("question", "")
    if not question:
        return {"error": "Falta el campo 'question'"}

    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=120) as cli:
        r = await cli.post(f"{OLLAMA}/api/generate", json={
            "model": MODEL,
            "prompt": f"<s>[INST] {question} [/INST]",
            "system": SYS_PROMPT,
            "options": {"temperature": TEMP, "num_predict": MAX_TOK},
            "stream": False
        })
    r.raise_for_status()
    data = r.json()
    latency_ms = int((time.perf_counter()-t0)*1000)

    return {
        "answer": data.get("response", ""),
        "latency_ms": latency_ms,
        "model": MODEL
    }
