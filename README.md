# Ahoum Sessions Marketplace

## Setup Instructions

### Environment Variables
1. Create a `.env` file in the root directory using the provided `.env.example` as a template.
2. Fill in your PostgreSQL database credentials and Django secret key.

### OAuth Client Setup
To enable Google and GitHub login:
1. **Google**: Go to the Google Cloud Console, create a new OAuth 2.0 Client ID for a Web Application. 
   - Authorized JavaScript origins: `http://localhost:3000`
   - Authorized redirect URIs: `http://localhost:3000/auth/callback`
   - Copy the Client ID and Secret to `.env`.
2. **GitHub**: Go to GitHub Developer Settings > OAuth Apps > New OAuth App.
   - Homepage URL: `http://localhost:3000`
   - Authorization callback URL: `http://localhost:3000/auth/callback`
   - Copy the Client ID and Secret to `.env`.

### Docker Commands (Quick Start)
To start the entire application (Frontend, Backend, Database, Nginx reverse proxy):
```bash
docker-compose up --build
```
*Frontend runs on localhost:3000, Backend on localhost:8000*

### Example Demo Flow
1. Open `http://localhost:3000`.
2. Click "Login" and sign in with Google or GitHub.
3. Switch your role to "Creator" in your profile tab.
4. Go to the Creator Dashboard and create a new session.
5. Go back to the homepage and book your session!
