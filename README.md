# Test Assignment for AI Digital

This repository contains a Dockerized application consisting of three containers:  
**ETL**, **Dashboard**, and **PostgreSQL database**.

---

### Project Overview
1. The **database** container starts first and creates a persistent PostgreSQL instance.  
2. The **ETL** container runs automatically after the database is ready — it downloads data about countries from the REST Countries API and loads it into the database.  
3. The **Dashboard** container launches a Dash web application that visualizes the data from the database in a sortable table with country flags.

Once all containers are running, you can open the dashboard in your browser.

---

### How to Run the Project

In the project root directory (`root`), run the following command:

```bash
docker-compose up --build -d
```

This will:
- Build Docker images for ETL and Dashboard;
- Start the PostgreSQL database;
- Run the ETL process;
- Launch the Dash web interface.

After startup, open your browser at:  
[http://localhost:8050](http://localhost:8050)

---

### How to Stop the Project

To stop and remove all containers, volumes, and networks created by Docker Compose, run:

```bash
docker-compose down -v
```

---

### Notes
- For this assignment, I selected slightly more fields from the API than in the example.
A detailed description of which data was extracted and how it was transformed can be found in `etl_app/transform.py`.
- I know that relational databases like PostgreSQL are not the best choice for dashboard applications — columnar databases are usually more suitable.  
However, I chose PostgreSQL because it’s easy to work with and the dataset from the API is quite small.
- Make sure Docker and Docker Compose are installed on your system.  
- The first run might take a few minutes since Docker needs to build images and install dependencies.

---

### Containers
| Container | Description |
|------------|--------------|
| **db** | PostgreSQL database used for persistent storage |
| **etl_app** | Python ETL script that fetches data and loads it into the database |
| **dashboard_app** | Dash application that displays data with flags |

---

### Environment Variables
The project uses environment variables defined in the `.env` file.  

