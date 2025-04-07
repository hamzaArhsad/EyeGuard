FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

# Change the host to 0.0.0.0 to allow external connections
CMD ["python", "-c", "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=5001, debug=True)"] 