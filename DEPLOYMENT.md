# SIH26070 — Deployment & Cloud Hosting Guide

This guide provides instructions for deploying the **Cyclone AI/ML System** using Docker and the best **100% free cloud platforms** for the Smart India Hackathon (SIH 2026).

---

## 1. Best Free Cloud Option for SIH: Hugging Face Spaces (Docker)

### Why Hugging Face Spaces is Best for SIH:
- **100% Free**: No credit card required.
- **Resource Limits**: **2 vCPUs, 16 GB RAM, 50 GB disk** (plenty of RAM for PyTorch, ResNet, and Transformers).
- **Persistent Public URL**: Unlike Render, it **does not go to sleep after 15 minutes**. Your API and Swagger UI will be instantly accessible when judges test it on their phones or laptops.
- **HTTPS & Custom Subdomain**: `https://<your-username>-cyclone-ai.hf.space/docs`

### How to Deploy to Hugging Face Spaces (3 Steps):
1. Sign up at [huggingface.co](https://huggingface.co/) (free).
2. Click **New Space** $\rightarrow$ Space Name: `cyclone-ai` $\rightarrow$ License: `MIT` $\rightarrow$ Select **Docker** (Blank).
3. Clone the repo and push your files:
   ```bash
   git clone https://huggingface.co/spaces/<your-username>/cyclone-ai
   cd cyclone-ai
   # Copy Dockerfile, requirements.txt, src/, data/, models/, run.py
   git add .
   git commit -m "Deploy Cyclone AI/ML system"
   git push
   ```
4. Hugging Face will automatically build the container and provide your live public URL!

---

## 2. Free Cloud Option 2: Render (Docker Web Service)

1. Sign up at [render.com](https://render.com/).
2. Create **New Web Service** $\rightarrow$ Connect your GitHub repo.
3. Select **Docker** environment $\rightarrow$ Choose **Free Tier**.
4. Set Port: `8000`.
5. Click **Create Web Service**.
*(Note: Render free tier spins down after 15 minutes of inactivity and takes ~50s to wake up on the next request).*

---

## 3. Local / On-Premise Demo (Offline in Hackathon Room)

If the hackathon venue has poor or no Wi-Fi, you can run the entire multi-container production stack locally via Docker Compose:

```bash
docker compose up --build
```

This starts:
- **FastAPI Backend**: `http://localhost:8000` (Swagger UI at `/docs`)
- **PostgreSQL + PostGIS**: `localhost:5432` with spatial extensions
