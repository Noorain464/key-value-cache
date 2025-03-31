Key-Value Cache Service
This project implements an in-memory key-value store with basic PUT and GET operations, designed to handle high loads efficiently while maintaining low latency.

Features
In-Memory Cache: Uses an LRU (Least Recently Used) eviction policy.

Memory Management: Automatically evicts items when memory usage exceeds 70%.

REST API: Implements endpoints for adding, retrieving, and checking service health.

Performance Optimized: Designed to handle thousands of requests per second on limited hardware (AWS t3.small).

API Endpoints
PUT Operation

HTTP Method: POST

Endpoint: /put

Request Body:

json
{
  "key": "string (max 256 characters)",
  "value": "string (max 256 characters)"
}
Response:

On Success (HTTP 200):

json
{
  "status": "OK",
  "message": "Key inserted/updated successfully."
}
On Failure (HTTP 400):

json
{
  "status": "ERROR",
  "message": "Key/Value exceeds 256 characters"
}
GET Operation

HTTP Method: GET

Endpoint: /get

Query Parameter: key

Response:

On Success (HTTP 200):

json
{
  "status": "OK",
  "key": "<key>",
  "value": "<value>"
}
If Key Not Found (HTTP 404):

json
{
  "status": "ERROR",
  "message": "Key not found."
}

Setup Instructions
Clone the repository:

Build the Docker image:

bash
docker build -t key-value-cache .
Run the Docker container:

bash
docker run -p 7171:7171 key-value-cache
Test the API using tools like Postman or curl.