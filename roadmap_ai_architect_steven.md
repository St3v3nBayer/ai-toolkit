# Roadmap: AI Architect + AWS SAA → Gen AI Developer
**Estudiante:** St3v3nBayer  
**Inicio:** Lunes 1 de junio de 2026  
**Duración estimada:** 12–15 semanas  
**Ritmo:** 2h SAA + 2h Python/IA por día (lunes a viernes) + 2h integración sábados

---

## Certificaciones (estado actual)

| Certificación | Estado |
|---|---|
| AWS Cloud Practitioner | ✅ Obtenida |
| AWS AI Practitioner | ✅ Obtenida |
| AWS SAA-C03 | 🔄 En curso |
| AWS Generative AI Developer | 🎯 Próxima meta |
| AWS ML Specialty | 🎯 Futuro |

---

## Recursos comprados / por comprar

| Recurso | Plataforma | Para qué |
|---|---|---|
| Ultimate AWS SAA-C03 — Stéphane Maarek | Udemy (esperar oferta ~$10-15) | Teoría SAA |
| AWS SAA-C03 Practice Exams — TutorialsDojo | portal.tutorialsdojo.com (~$15-20) | Práctica de examen |
| Sampler gratuito (30 preguntas) | portal.tutorialsdojo.com | Gratis, antes de comprar |

---

## Setup de entorno (completado)

- **OS:** Windows con WSL (Ubuntu)
- **Python:** 3.12 en WSL
- **Gestor de paquetes:** Poetry (reemplaza venv)
- **Editor:** VS Code conectado a WSL (`code .` desde terminal)
- **Herramientas:** black, ruff, pytest
- **Repo base:** `ai-toolkit` en GitHub (https://github.com/St3v3nBayer/ai-toolkit)

### Comandos clave de Poetry
```bash
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Crear proyecto nuevo
poetry new nombre-proyecto
cd nombre-proyecto

# Agregar dependencias
poetry add pydantic pytest black ruff

# Activar entorno
poetry shell

# Correr sin activar
poetry run python script.py
poetry run pytest
```

---

## Método de estudio Python (importante)

1. **40 min — Escribe tú solo, sin IA**
2. **30 min — Usa la IA como revisor** ("¿qué mejorarías y por qué?")
3. **30 min — Reescribe desde cero** aplicando lo aprendido
4. **20 min diarios — Lee código real** (LangChain, FastAPI, Pydantic en GitHub)

### Los 3 niveles de comprensión
- **Nivel 1 (sem 1–3):** Leer y entender código ajeno
- **Nivel 2 (sem 4–8):** Corregir y adaptar código
- **Nivel 3 (sem 9–15):** Diseñar arquitectura del código

---

## Horario semanal

| Día | Bloque 1 (2h) | Bloque 2 (2h) |
|---|---|---|
| Lunes | SAA — teoría (Maarek) | Python — concepto nuevo |
| Martes | SAA — laboratorio Free Tier | Python — ejercicio práctico |
| Miércoles | SAA — 25-30 preguntas TutorialsDojo (Review Mode) | Python — continúa ejercicio |
| Jueves | SAA — repaso cruzado + Anki | Python — Docker + pytest |
| Viernes | SAA — simulacro cronometrado (Timed Mode) | Python — RAG / Bedrock |
| Sábado | Integración semanal (2h) — proyecto acumulativo + GitHub push | — |
| Domingo | Descanso obligatorio | — |

**Total:** ~22h/semana (10h SAA + 12h Python/IA)

---

## Habilidades Python más demandadas para AI Architect 2026

| Habilidad | Uso real | Fase |
|---|---|---|
| Pydantic v2 | Validación de outputs de LLMs | Sem 1–2 |
| FastAPI + async/await | APIs para modelos en producción | Sem 2–3 |
| pytest | Calidad del código | Sem 1+ |
| LangChain / LangGraph | Orquestación de agentes | Sem 5–7 |
| LlamaIndex | RAG e indexación de documentos | Sem 7 |
| boto3 + Bedrock SDK | AWS nativo para IA | Sem 8 |
| Docker | MLOps y deploy | Sem 4 |
| GitHub Actions (CI/CD) | Deploy automático | Sem 9+ |

---

## Fase 1 — Python base (semanas 1–4)

**Proyecto acumulativo:** `ai-toolkit`  
**Repo:** https://github.com/St3v3nBayer/ai-toolkit

### Semana 1 (1–6 junio) — Entorno + Pydantic base ✅ EN CURSO

| Día | SAA | Python/IA |
|---|---|---|
| Lunes 1 jun | Global Infrastructure (regiones, AZs, edge locations) | Setup entorno + crear repo ai-toolkit |
| Martes 2 jun | IAM completo + lab Free Tier (usuario, rol, política) | Modelo `DocumentRecord` con Pydantic v2 |
| Miércoles 3 jun | 25 preguntas TutorialsDojo — IAM (Review Mode) | Estructuras: listas, dicts, sets + normalización CSV |
| Jueves 4 jun | EC2 fundamentos + lanzar t2.micro Free Tier | Funciones, decoradores, try/except tipado + pytest |
| Viernes 5 jun | 30 preguntas mixtas Timed Mode + registrar score | Lectura de archivos: pathlib, csv, JSON |
| Sábado 6 jun | — | Integración: week01/ completo en GitHub con README |

**Entregables semana 1:**
- [ ] Repo `ai-toolkit` con estructura `week01/{models,utils,tests}`
- [ ] `week01/models/document.py` — `DocumentRecord` con Pydantic v2
- [ ] `week01/utils/` — función normalizadora de CSV
- [ ] `week01/tests/` — mínimo 3 tests con pytest
- [ ] IAM: usuario + rol creado en Free Tier
- [ ] EC2: instancia t2.micro lanzada y terminada
- [ ] Score inicial TutorialsDojo registrado

### Modelo DocumentRecord (versión actual — semana 1)

```python
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator

# str que no acepta vacíos ni solo espacios
NonEmptyStr = Annotated[str, Field(min_length=1, strip_whitespace=True)]

# valores válidos para source
SourceType = Literal["pdf", "web", "csv", "manual"]

class DocumentRecord(BaseModel):
    model_config = {"frozen": False, "str_strip_whitespace": True}

    id: str = Field(default_factory=lambda: str(uuid4()))
    title: NonEmptyStr
    content: Annotated[str, Field(min_length=10)]
    source: SourceType
    language: str = "es"
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )

    @field_validator("tags")
    @classmethod
    def remove_duplicate_tags(cls, tags: list[str]) -> list[str]:
        seen = []
        for tag in tags:
            if tag not in seen:
                seen.append(tag)
        return seen

    @field_validator("content")
    @classmethod
    def content_not_only_spaces(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("content no puede ser solo espacios")
        return v.strip()
```

### Semana 2 (8–13 junio) — APIs REST + S3

| Día | SAA | Python/IA |
|---|---|---|
| Lunes | S3 fundamentos + storage classes | FastAPI: primer endpoint async |
| Martes | S3 lab: bucket, policies, versioning | FastAPI: endpoint que consume API externa (NewsAPI o similar) |
| Miércoles | 25 preguntas S3 (Review Mode) | Pydantic: validar respuesta de la API externa |
| Jueves | EBS, EFS, Instance Store | Docker: Dockerfile para la FastAPI |
| Viernes | Simulacro 30 preguntas (S3 + EC2 + IAM) | Integrar DocumentRecord con la API |
| Sábado | — | week02/ en GitHub: FastAPI + Docker + tests |

### Semana 3 (15–20 junio) — Bases de datos AWS + Pandas

| Día | SAA | Python/IA |
|---|---|---|
| Lunes | RDS: motores, Multi-AZ, Read Replicas | NumPy y Pandas: análisis de dataset CSV |
| Martes | RDS lab: crear instancia, conectar | Pandas: limpieza y estadísticas |
| Miércoles | 25 preguntas RDS (Review Mode) | Matplotlib: visualizar tendencias |
| Jueves | DynamoDB fundamentos | Exportar análisis a JSON estructurado |
| Viernes | Simulacro 30 preguntas | Integrar pipeline CSV → análisis → DocumentRecord |
| Sábado | — | week03/ en GitHub |

### Semana 4 (22–27 junio) — VPC + Testing avanzado

| Día | SAA | Python/IA |
|---|---|---|
| Lunes | VPC: subnets, route tables, IGW | pytest avanzado: fixtures, parametrize |
| Martes | VPC lab: crear VPC completa desde cero | Decoradores avanzados + context managers |
| Miércoles | 25 preguntas VPC (Review Mode) | Testing del pipeline completo del toolkit |
| Jueves | Security Groups vs NACLs | Estructura final del ai-toolkit: refactor |
| Viernes | Simulacro 40 preguntas (todos los temas) | Documentación con docstrings |
| Sábado | — | **ai-toolkit v1.0** — README principal completo, todos los módulos testeados |

---

## Fase 2 — Frameworks de IA (semanas 5–9)

**Proyecto acumulativo:** `smart-assistant`  
Chatbot con memoria y RAG conectado a AWS Bedrock

### Semana 5 — LangChain básico
- SAA: ELB, Auto Scaling, Route 53
- IA: LangChain chains, prompts, output parsers con Pydantic

### Semana 6 — Memoria y agentes
- SAA: CloudFront, API Gateway
- IA: ConversationBufferMemory, ReAct agents con herramientas

### Semana 7 — RAG con LlamaIndex
- SAA: SQS, SNS, EventBridge
- IA: Indexar PDFs propios, ChromaDB o FAISS como vector store

### Semana 8 — AWS Bedrock SDK
- SAA: Lambda fundamentos + lab
- IA: boto3 + Bedrock InvokeModel, streaming, Knowledge Bases

### Semana 9 — FastAPI + Deploy
- SAA: ECS, ECR, Elastic Beanstalk
- IA: Exponer el assistant como API, dockerizar, subir a Lambda o App Runner
- **Entregable:** `smart-assistant` con demo GIF en README

---

## Fase 3 — Arquitectura de IA en AWS (semanas 10–15)

**Proyecto final:** `ai-document-platform`  
Plataforma serverless completa: S3 → Lambda → Bedrock → API → Cognito

### Semana 10 — Pipeline serverless
- SAA: S3 + Lambda + triggers
- IA: Ingesta automática: subir doc a S3 → Lambda → Bedrock Knowledge Base

### Semana 11 — Prompt engineering avanzado
- SAA: IAM avanzado: roles entre servicios, policies
- IA: Chain-of-thought, few-shot, evaluación con LLM-as-judge

### Semana 12 — Fine-tuning y Guardrails
- SAA: CloudWatch, X-Ray, CloudTrail
- IA: Bedrock Guardrails para filtros, intro a Custom Models

### Semana 13 — Observabilidad
- SAA: Repaso general + simulacros intensivos
- IA: CloudWatch custom metrics, LangSmith para trazas

### Semana 14 — Auth multi-tenant
- SAA: Simulacros intensivos (objetivo: >80% consistente)
- IA: Cognito + aislamiento por usuario

### Semana 15 — IaC + CI/CD
- SAA: **EXAMEN** (si score >85% en simulacros)
- IA: AWS CDK o SAM para infraestructura, GitHub Actions para deploy automático
- **Entregable:** `ai-document-platform` con diagrama de arquitectura, IaC, demo video

---

## Los 3 repositorios GitHub (historia para reclutadores)

| Repo | Demuestra | Fase |
|---|---|---|
| `ai-toolkit` | Python limpio, Pydantic, FastAPI, pytest, Docker | 1 |
| `smart-assistant` | LangChain, RAG, Bedrock, agentes, deploy | 2 |
| `ai-document-platform` | Arquitectura serverless real, IaC, CI/CD, auth, observabilidad | 3 |

---

## Overlap con AWS Generative AI Developer (próximo cert)

| Dominio del examen | Dónde lo practicas |
|---|---|
| Bedrock Knowledge Bases | Semana 7–8 |
| Bedrock Guardrails | Semana 12 |
| Prompt engineering | Semana 11 |
| Fine-tuning con Bedrock | Semana 12 |
| Agentes con LangChain | Semana 6 |
| Observabilidad de IA | Semana 13 |

---

## Señales de progreso Python

| Cuándo | Señal |
|---|---|
| Semana 2–3 | Lees tracebacks sin pánico — el error te dice exactamente dónde buscar |
| Semana 4–5 | Detectas código de la IA que funciona pero tiene problemas de performance o legibilidad |
| Semana 7–8 | Diseñas la estructura antes de escribir código |
| Semana 10+ | Le das contexto preciso a la IA, ella genera, tú revisas en 2 minutos |

---

## Cómo continuar esta guía en una nueva conversación

Pega este mensaje al inicio de la nueva conversación:

> "Estoy siguiendo un roadmap de 15 semanas para convertirme en AI Architect con AWS. Tengo el AI Practitioner y el Cloud Practitioner. Estoy en la [SEMANA X], estudiando [TEMA SAA] y [TEMA PYTHON/IA]. Mi último entregable fue [DESCRIPCIÓN]. Continúa guiándome desde aquí."

Y adjunta este archivo como referencia.

