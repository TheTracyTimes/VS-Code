# 🚀 Church Camp Analytics - Setup Guide

## Overview

This application is split into two parts:
- **Public Site**: Registration form accessible to everyone
- **Admin Dashboard**: Password-protected analytics and data management

## Prerequisites

- Node.js 18+ and npm
- MongoDB (local or MongoDB Atlas cloud)

## Installation

### 1. Clone and Install Dependencies

```bash
cd church-camp-analytics
npm install
```

### 2. Set Up MongoDB

#### Option A: Local MongoDB (Recommended for Development)

1. Install MongoDB on your machine:
   - **macOS**: `brew install mongodb-community`
   - **Ubuntu**: `sudo apt-get install mongodb`
   - **Windows**: Download from [mongodb.com](https://www.mongodb.com/try/download/community)

2. Start MongoDB:
   ```bash
   # macOS/Linux
   mongod

   # Windows
   mongod.exe
   ```

#### Option B: MongoDB Atlas (Cloud - Free Tier)

1. Create account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/church-camp`)
4. Update `.env` file with your connection string

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Server Configuration
PORT=5000

# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017/church-camp

# Admin Authentication
# Generate a new hash for production:
# node -e "console.log(require('bcryptjs').hashSync('your-password', 10))"
ADMIN_PASSWORD_HASH=$2a$10$xQZ1xQZ1xQZ1xQZ1xQZ1xO
JWT_SECRET=change-this-to-a-random-secret-key

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:5173
```

### 4. Run the Application

#### Development Mode (Both Frontend + Backend)

```bash
npm run dev
```

This starts:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

#### Run Separately

```bash
# Terminal 1 - Backend only
npm run server

# Terminal 2 - Frontend only
npm run client
```

## Usage

### For Public Users (Attendees)

1. Go to `http://localhost:5173`
2. Fill out the registration form
3. Submit and get redirected to payment page

### For Administrators

1. Go to `http://localhost:5173/admin`
2. Enter password: `admin123` (default)
3. View dashboard with all analytics

**⚠️ IMPORTANT**: Change the admin password before deploying to production!

## Changing Admin Password

### Method 1: Using Node.js

```bash
node -e "console.log(require('bcryptjs').hashSync('your-new-password', 10))"
```

Copy the output and update `ADMIN_PASSWORD_HASH` in `.env`

### Method 2: Using npm script (coming soon)

```bash
npm run set-admin-password
```

## Project Structure

```
church-camp-analytics/
├── server/                 # Backend (Node.js + Express)
│   ├── models/            # MongoDB schemas
│   ├── routes/            # API routes
│   └── index.js           # Server entry point
├── src/                   # Frontend (React + TypeScript)
│   ├── api/               # API client
│   ├── components/        # Reusable components
│   ├── context/           # React context (Auth)
│   ├── pages/             # Page components
│   └── App.tsx            # Main app with routing
└── .env                   # Environment variables
```

## API Endpoints

### Public Endpoints

- `POST /api/registrations` - Submit new registration
- `GET /api/registrations/count` - Get total registration count

### Admin Endpoints (Protected)

- `POST /api/admin/login` - Admin login
- `GET /api/admin/registrations` - Get all registrations
- `GET /api/admin/analytics` - Get calculated analytics
- `DELETE /api/admin/registrations/:id` - Delete registration

## Building for Production

```bash
npm run build
```

Output will be in the `dist/` folder.

## Deployment

### Backend Deployment (Heroku, Railway, etc.)

1. Set environment variables on your hosting platform
2. Run `node server/index.js`
3. Ensure MongoDB connection string is correct

### Frontend Deployment (Vercel, Netlify, etc.)

1. Build: `npm run build`
2. Deploy the `dist/` folder
3. Set `VITE_API_URL` to your backend URL

## Troubleshooting

### MongoDB Connection Error

- Ensure MongoDB is running: `mongod`
- Check connection string in `.env`
- For Atlas: Whitelist your IP address

### Port Already in Use

Change ports in `.env`:
```
PORT=3000  # Backend port
```

And update Vite config for frontend if needed.

### Admin Login Not Working

- Check that `ADMIN_PASSWORD_HASH` is set correctly
- Default password is `admin123`
- Clear browser localStorage and try again

## Support

For questions or issues:
- Email: contact@assemblee-laval.org
- Phone: (555) 123-4567

---

Built with ❤️ for Assemblée Évangélique de Laval
