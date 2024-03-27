# Meeting notes of first working session
Date: 2024-03-14
Time: 21:05 CET

# Updates

**Janine**
- Found that Firestore is significantly cheaper than using BigQuery
- Cloud SQL heavily depends on how much instance time is generated
- Using both Firestore and BigQuery is weird according to Cedric

Decision: we will just use BigQuery for every layer

**Mouad**
- Docker compose and Docker files does
- Sharing Python virtual environments using poetry
- Will commit changes to venv as pull request
- Will continue on local development setup for project

**Kevin**
- Did not show up

**Malte**
- Has set up BigQuery datasets and assigned access to Mouad and Janine
- However not sure how other collaborators can access his BQ datasets
- Has created Service Account with access to BigQuery
- TODO: Figure out how to grant collaborators access to BQ datasets
