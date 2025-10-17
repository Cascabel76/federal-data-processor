# Notes on Webcrawling in Python:
---
## Web Crawling with Requests:
In reference to GeeksforGeeks, the first step here is to fetch the content of the webpage, leveraging the Request library to send an HTTP request and retrieve the HTML content. 

* **request.get(URL)** sends a git request to the specified URL
* **response.status_code** checks if the request was sucessful status code 200 means sucess
* **response.text** contains the HTML content of the website

