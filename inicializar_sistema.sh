#!/din/bash
cd /home/servidorhsp
source entorno/bin/activate
cd backend_hsp
uvicorn api:app --host 0.0.0.0 --port 8000