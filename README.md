<p align="center">
  <img height="60" src="https://nux.ai/static/img/brand/nux_logo_dark.png" alt="NUX Logo">
</p>
<p align="center">
<strong><a href="https://docs.nux.ai/">Documentation</a> | <a href="https://www.nux.ai/newsletter-signup/">Email List</a>
</strong>
</p>

<p align="center">
    <a href="https://github.com/nux-ai/server/stargazers">
        <img src="https://img.shields.io/github/stars/nux-ai/server.svg?style=flat&color=yellow" alt="Github stars"/>
    </a>
    <a href="https://github.com/nux-ai/server/issues">
        <img src="https://img.shields.io/github/issues/nux-ai/server.svg?style=flat&color=success" alt="GitHub issues"/>
    </a>
    <a href="https://join.slack.com/t/nuxai/shared_invite/zt-2efp37o7q-FDyH3LFPkeOsc9Vi_Q6ZEA">
        <img src="https://img.shields.io/badge/slack-join-green.svg?logo=slack" alt="Join Slack"/>
    </a>
</p>

<h2 align="center">
    <b>real-time multi-modal vector embedding. set and forget. 
    </b>
</h2>

## Overview

NUX SDK is a cutting-edge solution designed to automate and streamline the handling of database changes, file processing, and data embedding. In the business-as-usual (BAU) scenario, tracking database changes, extracting content, processing it, and then integrating the processed data back into the database involves a considerable amount of manual effort and coordination. This not only slows down operations but also increases the risk of errors. NUX SDK addresses these challenges by offering an automated, scalable, and efficient way to manage these processes.

## Why NUX?

The need for NUX arises from the pain points experienced by businesses in managing database changes and processing data:

- **Manual Monitoring and Processing**: Manually monitoring for database changes and processing data is time-consuming and prone to error, affecting efficiency and reliability.
- **Scalability Issues**: Handling large volumes of data and spikes in database changes can be challenging without an automated, scalable system.
- **Integration Complexity**: Integrating processed data back into databases often requires custom solutions, complicating the overall data management strategy.

NUX automates these processes, providing a seamless, scalable solution that operates across four independent services, each running in its own Docker container. This architecture allows for independent scaling and ensures that a bottleneck in one service doesn't affect the others.

## Services Architecture

NUX is structured into four main services, each designed to handle a specific part of the process:

- **API (Orchestrator)**: Coordinates the flow between services, ensuring smooth operation and handling failures gracefully.
- **Listener**: Monitors the database for specified changes, triggering the process when changes are detected.
- **Parser**: Downloads and parses the changed files, preparing them for processing.
- **Embedder**: Processes the parsed data, generating embeddings that can then be integrated back into the database.

These services are containerized and can be deployed on separate servers for optimal performance and scalability.

## Getting Started

### Installation

Clone the NUX repository and navigate to the SDK directory:

```bash
git clone <NUX-repository-url>
cd <NUX-sdk-directory>
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Configuration and Usage

Configure each service with your environment's specifics. Here's an illustrative setup:

```python
# Listener Service Configuration
LISTENER_DB_CONFIG = {
    "dbname": "your_db_name",
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "your_db_host",
    "port": 5432
}

class InsertSchema:
    file_id: str
    embedding: list
    contents: str

# Example: Starting the Listener Service
from nux.listener import listen
listen("your_table_name", LISTENER_DB_CONFIG)

# API Service Invocation
# Example: Triggering the Parser and Embedder Services
from nux.api import trigger_services
trigger_services(file_url="http://example.com/yourfile.pdf", file_id="1234")
```

This fake code demonstrates how you might configure and use NUX SDK services. Replace placeholders with your actual data.

## Contributing

Contributions are welcome! Fork the repository, add your feature or bug fix, and submit a pull request.

## License

NUX SDK is licensed under the MIT License.

## Conclusion

NUX SDK revolutionizes how businesses interact with their databases, automating the monitoring, processing, and embedding of data. This automation not only alleviates manual labor but also significantly enhances data processing efficiency and reliability. By deploying each service in its own Docker container, NUX ensures scalability and flexibility, adapting to your business's growing needs.