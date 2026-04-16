# N8n Newsletter — Automated AI News Digest

Pipeline automatizado de generación de newsletters usando **n8n**, **OpenAI**, **Serper** y **PostgreSQL con pgvector**. El sistema busca, scraping, analiza y deduplica noticias relevantes para una empresa objetivo, generando reportes HTML listos para distribución.

---

## Arquitectura

```
Serper API (búsqueda)
       │
       ▼
   n8n Workflow
       │
       ├── Python Scraper (extracción de contenido)
       │
       ├── OpenAI (análisis y redacción)
       │
       └── PostgreSQL + pgvector (deduplicación semántica)
                │
                ▼
           Reporte HTML (output/)
```

---

## Stack

| Componente | Tecnología |
|---|---|
| Orquestación | [n8n](https://n8n.io) |
| IA / Análisis | OpenAI API |
| Búsqueda web | Serper API |
| Base de datos | PostgreSQL + pgvector |
| Scraping | Python (Trafilatura, BeautifulSoup) |
| Infraestructura | Docker + Docker Compose |

---

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Claves de API: OpenAI y Serper

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JavierGior/N8n_Newsleter.git
cd N8n_Newsleter
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Completar `.env` con las claves reales. Ver [.env.example](.env.example) para referencia.

### 3. Levantar los servicios

```bash
docker compose up -d
```

Esto inicia PostgreSQL y n8n en [http://localhost:5678](http://localhost:5678).

### 4. Importar el workflow

1. Abrí n8n en [http://localhost:5678](http://localhost:5678)
2. Ir a **Workflows → Import from file**
3. Seleccionar `Gemini_n8n_Newsleter.json`
4. Configurar las credenciales de OpenAI, Serper y PostgreSQL en n8n

---

## Uso

### Ejecutar el workflow

Desde n8n, abrir el workflow y hacer clic en **Test workflow**. Los reportes HTML se generan en `output/`.

### Auditoría de reportes

Para verificar URLs activas y relevancia de las noticias generadas:

```bash
pip install aiohttp beautifulsoup4
python validacion-py
```

Genera un CSV con el análisis de cada URL del reporte.

---

## Estructura del proyecto

```
N8n_Newsleter/
├── python_scripts/
│   └── scraper_n8n.py              # Scraper de contenido web
├── .env.example                    # Template de variables de entorno
├── docker-compose.yml              # Orquestación de servicios
├── Dockerfile                      # Imagen n8n + Python
├── Gemini_n8n_Newsleter.json       # Workflow principal de n8n
├── init-db.sql                     # Schema inicial de PostgreSQL
└── validacion-py                   # Script de auditoría de reportes
```

---

## ✒️ Autor

**Javier Giordano** — [Perfil de LinkedIn](https://www.linkedin.com/in/javier-giordano/) · [javiergiordano.com.ar](https://www.javiergiordano.com.ar/)
