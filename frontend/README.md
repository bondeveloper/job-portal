# Job Portal Frontend

A React + TypeScript frontend for the Job Portal application.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router** - Navigation
- **TanStack Query** - Data fetching
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

### Development

Run the development server (runs on http://localhost:3000):
```bash
npm run dev
```

The frontend is configured to proxy API requests to `http://localhost:8000/api`.

### Build

Build for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── layouts/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   ├── styles/
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── vite.config.ts
├── tsconfig.json
└── tailwind.config.js
```

## API Integration

API calls are made through the `services/api.ts` client, which automatically:
- Adds the auth token to all requests
- Handles 401 errors by redirecting to login

## Authentication

Auth tokens are stored in localStorage and sent with every API request via the `Authorization: Bearer <token>` header.
