# Banco Pichincha - DevOps Technical Assessment

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

Microservicio REST en Python (FastAPI) con arquitectura limpia, observabilidad, y despliegue containerizado siguiendo las mejores prácticas de DevOps.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Inicio Rápido](#-inicio-rápido)
- [Subir a GitHub](#-subir-a-github)
- [Endpoints](#-endpoints)
- [Probar Localmente](#-probar-localmente)
- [Docker](#-docker)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Infraestructura](#-infraestructura)

---

## 🔧 Requisitos Previos

- **Python** 3.10 o superior
- **pip** (gestor de paquetes de Python)
- **Docker** (opcional, para contenedores)
- **Helm 3** (opcional, para Kubernetes)
- **Git** (para versionado)

---

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/<tu-usuario>/banco-devops-assessment.git
cd banco-devops-assessment
```

### 2. Instalar dependencias
```bash
make install
```
> Esto instala el proyecto en modo editable con dependencias de desarrollo.

### 3. Ejecutar la aplicación
```bash
make run
```
La API estará disponible en: **http://localhost:8000**

### 4. Ejecutar tests
```bash
make test
```

---

## 📤 Subir a GitHub

### Inicializar repositorio y subir por primera vez
```bash
# Inicializar git (si aún no está inicializado)
git init

# Agregar todos los archivos
git add .

# Crear commit inicial
git commit -m "feat: Initial DevOps Assessment implementation"

# Agregar remote (reemplaza con tu URL)
git remote add origin https://github.com/<tu-usuario>/banco-devops-assessment.git

# Subir a GitHub
git branch -M main
git push -u origin main
```

### Subir cambios posteriores
```bash
git add .
git commit -m "descripción del cambio"
git push
```

---

## 📡 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/DevOps` | Procesa mensajes (requiere autenticación) |
| `GET` | `/healthz` | Liveness probe |
| `GET` | `/readyz` | Readiness probe |
| `GET` | `/metrics` | Métricas Prometheus |
| `GET` | `/docs` | Swagger UI (Documentación interactiva) |

---

## 🧪 Probar Localmente

### Opción 1: Ejecutar directamente con Python

```bash
# Instalar dependencias
make install

# Iniciar servidor de desarrollo
make run
```

### Opción 2: Ejecutar con Docker

```bash
# Construir imagen
make docker-build

# Ejecutar contenedor
docker run -p 8000:8000 devops-service:latest
```

### Probar el endpoint principal

Una vez la aplicación esté corriendo, usar este comando `curl`:

```bash
curl -X POST http://localhost:8000/DevOps \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: tu-token-jwt-aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45
  }'
```

**Respuesta esperada:**
```json
{"message": "Hello Juan Perez your message will be send"}
```

### Probar otros métodos HTTP (debe retornar "ERROR")

```bash
curl -X GET http://localhost:8000/DevOps \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: cualquier-token"
```
**Respuesta esperada:** `"ERROR"` (Status 405)

### Verificar Health Checks

```bash
# Liveness
curl http://localhost:8000/healthz

# Readiness  
curl http://localhost:8000/readyz

# Métricas Prometheus
curl http://localhost:8000/metrics
```

---

## 🐳 Docker

### Construir la imagen
```bash
make docker-build
# o directamente:
docker build -t devops-service:latest .
```

### Ejecutar el contenedor
```bash
docker run -d -p 8000:8000 --name devops-api devops-service:latest
```

### Verificar que corre como non-root
```bash
docker exec devops-api whoami
# Debe mostrar: nonroot (o UID 65532)
```

---

## 📁 Estructura del Proyecto

```
.
├── src/                    # Código fuente
│   ├── main.py             # Entrypoint de la aplicación
│   ├── core/               # Configuración y seguridad
│   ├── models/             # Modelos Pydantic
│   ├── routers/            # Definición de endpoints
│   ├── services/           # Lógica de negocio
│   └── utils/              # Utilidades (logging)
├── tests/                  # Suite de tests (pytest)
├── chart/                  # Helm Chart para Kubernetes
│   ├── templates/          # Manifiestos K8s templados
│   └── values.yaml         # Valores configurables
├── terraform/              # IaC para GKE/Registry
├── .github/workflows/      # Pipeline CI/CD
├── Dockerfile              # Multi-stage, Distroless
├── Makefile                # Comandos útiles
├── pyproject.toml          # Configuración del proyecto
└── README.md               # Este archivo
```

---

## 🔄 CI/CD Pipeline

El pipeline de GitHub Actions (`.github/workflows/pipeline.yml`) ejecuta:

1. **Lint & Test**: Ruff + Black + Pytest
2. **Security Scan**: Bandit (código) + Trivy (imagen)
3. **Build & Push**: Construcción de imagen Docker
4. **Deploy**: Helm upgrade (dry-run)

---

## ☁️ Infraestructura

### Helm Chart

Desplegar en Kubernetes:
```bash
helm install devops-api ./chart --namespace default
```

Validar templates:
```bash
helm template ./chart
```

### Terraform (GKE)

```bash
cd terraform
terraform init
terraform plan -var="project_id=tu-proyecto-gcp"
terraform apply
```

---

## 🛠️ Comandos Makefile

| Comando | Descripción |
|---------|-------------|
| `make install` | Instala dependencias de desarrollo |
| `make test` | Ejecuta tests con pytest |
| `make lint` | Verifica código con ruff y black |
| `make format` | Formatea código automáticamente |
| `make run` | Inicia servidor de desarrollo |
| `make docker-build` | Construye imagen Docker |
| `make security-scan` | Escanea código con Bandit |

---

## 🔐 Autenticación

El endpoint `/DevOps` requiere los siguientes headers:

| Header | Valor |
|--------|-------|
| `X-Parse-REST-API-Key` | `2f5ae96c-b558-4c7b-a590-a501ae1c3f6c` |
| `X-JWT-KWY` | Cualquier token JWT válido |

---

## 📄 Licencia

Este proyecto es parte de una evaluación técnica para Banco Pichincha.
