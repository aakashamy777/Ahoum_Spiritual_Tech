# Ahoum Sessions Marketplace

## Tech Stack
- Frontend: Next.js 14, TypeScript, TailwindCSS
- Backend: Django 4.2 + DRF, PostgreSQL 15
- Infrastructure: Docker, Nginx, JWT auth

## Quick Start
1. Clone repo
2. `cp .env.example .env` — fill in values
3. `docker-compose up --build`
4. Visit http://localhost

## OAuth Setup
### Google:
- Go to console.cloud.google.com → Create project → OAuth 2.0 credentials
- Authorized redirect URI: http://localhost/api/auth/google/callback/
- Copy Client ID + Secret to `.env`

### GitHub:
- Settings → Developer Settings → OAuth Apps → New
- Callback URL: http://localhost/api/auth/github/callback/
- Copy Client ID + Secret to `.env`

## Demo Flow
1. Visit http://localhost → Browse session catalog
2. Click any session → View detail
3. "Login with Google" → OAuth flow → JWT issued
4. Book a session → appears in User Dashboard
5. Switch role to Creator → go to `/creator`
6. Create a session → appears in public catalog
7. View bookings on Creator Dashboard

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/google/` | Public | Google OAuth login |
| POST | `/api/auth/github/` | Public | GitHub OAuth login |
| POST | `/api/auth/refresh/` | Public | Refresh JWT |
| GET/PATCH | `/api/auth/me/` | JWT | Get/Update user profile |
| GET | `/api/sessions/` | Public | List sessions (paginated, filtered) |
| GET | `/api/sessions/<id>/` | Public | View session details |
| POST | `/api/sessions/` | Creator | Create a new session |
| PATCH/DEL | `/api/sessions/<id>/` | Creator | Edit/Delete own session |
| POST | `/api/bookings/` | JWT | Book a session |
| GET | `/api/bookings/my/` | JWT | List user's bookings |
| PATCH | `/api/bookings/<id>/cancel/` | JWT | Cancel a booking |
| GET | `/api/bookings/creator-overview/` | Creator | Creator's bookings overview |
| POST | `/api/payments/create-order/` | JWT | Create Razorpay order |
| POST | `/api/payments/verify/` | JWT | Verify Razorpay payment |

## Architecture
```text
           +-------------+
           |   Browser   |
           +------+------+
                  | HTTP/HTTPS
           +------v------+
           |    Nginx    | (Reverse Proxy)
           +--+-------+--+
              |       |
      /api/*  |       | / (Next.js routing)
              v       v
+-------------+-+   +-+-------------+
|    Backend    |   |   Frontend    |
| (Django+DRF)  |   |  (Next.js 14) |
+------+--------+   +---------------+
       |
       v
+-------------+
| PostgreSQL  |
+-------------+
```
