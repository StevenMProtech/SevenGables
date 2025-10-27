# Seven Gables Real Estate - Email Campaign System

A professional email campaign and lead management system for Seven Gables Real Estate's "Your Next Chapter" campaign.

## Features

- **Interactive Email Template**: Beautiful, responsive email design with form submission
- **Dashboard**: Real-time analytics and campaign preview
- **Lead Management**: Track submissions, priorities, and client goals
- **Data Export**: Export submissions to CSV for CRM integration
- **API Access**: JSON API for programmatic access to submission data

## Campaign Overview

**Target**: Past clients in Southern California  
**Value Proposition**: $583k-$788k estimated home equity  
**Key Programs**:
- SG Refresh Program (complimentary staging)
- JamesEdition luxury marketing
- 49 years of Southern California expertise

## Quick Start

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
python app.py
```

3. **Access the Dashboard**
- Dashboard: http://localhost:5000
- Email Preview: http://localhost:5000/test
- Submissions: http://localhost:5000/submissions

### Deploy to Render

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit - Seven Gables campaign"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

2. **Connect to Render**
- Go to [render.com](https://render.com)
- Create new Web Service
- Connect your GitHub repository
- Render will auto-detect `render.yaml` and deploy

3. **Update Form Action**
- After deployment, update the form action URL in `email_template.html`
- Change `https://metrobrokers.onrender.com/api/submit` to your Render URL

## Project Structure

```
.
├── app.py                    # Flask application
├── email_template.html       # Seven Gables email template
├── requirements.txt          # Python dependencies
├── render.yaml              # Render deployment config
├── submissions.json         # Lead data storage (auto-created)
└── README.md               # This file
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard with analytics |
| `/test` | GET | Email template preview |
| `/api/submit` | POST | Form submission endpoint |
| `/submissions` | GET | View all submissions |
| `/api/submissions` | GET | JSON API for submissions |
| `/export` | GET | Download CSV export |

## Form Fields

**Hidden Fields** (auto-populated from HubSpot):
- `email`
- `firstName`
- `lastName`

**User Input**:
- `equity_priority`: maximize, speed, balance, exploring
- `goals[]`: upsize, downsize, relocate, second-home, investment, help-family, life-transition, curious
- `goalsText`: Optional text area
- `phoneNumber`: Contact number
- `wantsReport`: Checkbox (market analysis)
- `wantsExpert`: Checkbox (advisor reconnect)

## Customization

### Update Company Information

Edit the footer section in `email_template.html`:
```html
{{ site_settings.company_name }}
{{ site_settings.company_street_address_1 }}
{{ site_settings.company_city }}, {{ site_settings.company_state }} {{ site_settings.company_zip }}
```

### Change Color Scheme

Primary colors used:
- Dark Blue: `#2c3e50`
- Gold: `#d4af37`
- Light Gray: `#fafafa`

### Add Logo

Replace the logo placeholder in `email_template.html`:
```html
<img src="sevengables_logo.png" alt="Seven Gables Real Estate" style="width: 200px; height: auto;" />
```

## HubSpot Integration

This template uses HubSpot personalization tokens:
- `{{ contact.firstname }}`
- `{{ contact.lastname }}`
- `{{ contact.email }}`
- `{{ contact.phone }}`
- `{{ site_settings.company_name }}`
- `{{ unsubscribe_link }}`
- `{{ unsubscribe_link_all }}`

## Analytics Tracked

- Total submissions
- Pending reviews
- Priority distribution (maximize/speed/balance/exploring)
- Goal selections
- Contact preferences

## Brand Identity

### Colors
- **Primary**: Dark Blue (#2c3e50) - Professional and trustworthy
- **Accent**: Gold (#d4af37) - Luxury and sophistication
- **Background**: Light Gray (#fafafa) - Clean and modern

### Tagline
**"We Never Settle & Never Follow"** - Seven Gables Real Estate

### Company Stats
- **Founded**: 1976
- **Experience**: 49 years of Southern California expertise
- **Sales Volume**: $2.28 billion over the past 12 months
- **Advisor Experience**: Average of 10 years per advisor

## Deployment Options

### Option 1: Render.com (Recommended - Free)

1. Push this folder to a GitHub repository
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Render will auto-detect the `render.yaml` config
6. Click "Create Web Service"
7. Your app will be live at: `https://your-app.onrender.com`

### Option 2: Railway.app (Free)

1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Railway will auto-detect Python and deploy
6. Get your live URL from the dashboard

### Option 3: Vercel (Free)

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts
4. Your app will be live

### Option 4: PythonAnywhere (Free)

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create free account
3. Upload files via "Files" tab
4. Set up web app pointing to `app.py`
5. Install requirements: `pip install -r requirements.txt`

## Technical Stack

- **Backend**: Python 3.11 + Flask
- **Frontend**: HTML/CSS (email-safe inline styles)
- **Storage**: JSON file (upgradeable to SQL)
- **Deployment**: Render/Railway/Vercel/PythonAnywhere

## Data Storage

Uses simple JSON file storage (`submissions.json`). For production with high volume, consider upgrading to PostgreSQL or MongoDB.

## Support

For questions or customization needs, contact your development team.

## License

© 2025 Seven Gables Real Estate. All rights reserved.

---

**Built for Seven Gables Real Estate** | Southern California | Since 1976

