FROM python:3.11-slim

# Set environment
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --default-timeout=300 --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

CMD ["bash"]
