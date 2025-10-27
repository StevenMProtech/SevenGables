from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

SUBMISSIONS_FILE = 'submissions.json'

def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, 'w') as f:
        json.dump(submissions, f, indent=2)

@app.route('/test')
def test_page():
    with open('email_template.html', 'r') as f:
        email_html = f.read()
    return email_html

@app.route('/')
def index():
    submissions = load_submissions()
    total = len(submissions)
    pending = sum(1 for s in submissions if s.get('status') == 'pending')
    maximize = sum(1 for s in submissions if s.get('equity_priority') == 'maximize')
    speed = sum(1 for s in submissions if s.get('equity_priority') == 'speed')
    balance = sum(1 for s in submissions if s.get('equity_priority') == 'balance')
    exploring = sum(1 for s in submissions if s.get('equity_priority') == 'exploring')
    
    # Load email template
    with open('email_template.html', 'r') as f:
        email_html = f.read()
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Seven Gables Real Estate Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #1a1a1a;
            min-height: 100vh;
        }}
        .dashboard {{
            display: grid;
            grid-template-columns: 350px 1fr;
            height: 100vh;
        }}
        .sidebar {{
            background: linear-gradient(180deg, #3d3430 0%, #2a2520 100%);
            border-right: 1px solid #d4af37;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}
        .sidebar-header {{
            padding: 30px 30px 20px;
            flex-shrink: 0;
        }}
        .sidebar-stats {{
            flex: 1;
            overflow-y: auto;
            padding: 0 30px;
        }}
        .sidebar-stats::-webkit-scrollbar {{
            width: 6px;
        }}
        .sidebar-stats::-webkit-scrollbar-track {{
            background: rgba(212, 175, 55, 0.1);
        }}
        .sidebar-stats::-webkit-scrollbar-thumb {{
            background: rgba(212, 175, 55, 0.5);
            border-radius: 3px;
        }}
        .sidebar-stats::-webkit-scrollbar-thumb:hover {{
            background: rgba(212, 175, 55, 0.7);
        }}
        .logo {{
            font-size: 28px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
            font-family: Georgia, serif;
        }}
        .logo span {{ color: #d4af37; }}
        .tagline {{
            color: #e8e3dd;
            font-size: 14px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(212, 175, 55, 0.3);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .stat-card {{
            background: rgba(212, 175, 55, 0.1);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 3px solid #d4af37;
        }}
        .stat-card h3 {{
            color: #e8e3dd;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .stat-card .number {{
            font-size: 36px;
            font-weight: 700;
            color: #d4af37;
            line-height: 1;
        }}
        .stat-card .label {{
            color: #d0c5b8;
            font-size: 12px;
            margin-top: 5px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .actions {{
            padding: 20px 30px 30px;
            border-top: 1px solid rgba(212, 175, 55, 0.3);
            flex-shrink: 0;
            background: linear-gradient(180deg, transparent 0%, rgba(42, 37, 32, 0.8) 20%, #2a2520 100%);
        }}
        .actions h3 {{
            color: white;
            font-size: 14px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .btn {{
            display: block;
            padding: 12px 20px;
            background: linear-gradient(135deg, #d4af37 0%, #c9a22e 100%);
            color: #6b5d52;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin-bottom: 10px;
            text-align: center;
            transition: all 0.2s;
            font-size: 14px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .btn:hover {{ transform: translateX(5px); }}
        .btn.secondary {{
            background: linear-gradient(135deg, #8b7d72 0%, #6b5d52 100%);
            color: #d4af37;
        }}
        .btn.outline {{
            background: transparent;
            border: 2px solid #d4af37;
            color: #d4af37;
        }}
        .preview {{
            background: #f5f5f5;
            overflow-y: auto;
            padding: 40px 20px;
        }}
        .preview-header {{
            background: white;
            padding: 20px 30px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .preview-header h2 {{
            color: #333;
            font-size: 20px;
            font-family: Georgia, serif;
        }}
        .preview-header .badge {{
            background: #d4af37;
            color: #6b5d52;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .zoom-controls {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}
        .zoom-btn {{
            background: #f0f0f0;
            border: 1px solid #ddd;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .zoom-btn:hover {{
            background: #e0e0e0;
        }}
        .zoom-level {{
            font-size: 12px;
            color: #d0c5b8;
            min-width: 45px;
            text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        .email-container {{
            max-width: 650px;
            margin: 0 auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        @media (max-width: 1024px) {{
            .dashboard {{
                grid-template-columns: 1fr;
            }}
            .sidebar {{
                border-right: none;
                border-bottom: 1px solid #d4af37;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="sidebar">
            <div class="sidebar-header">
                <img src="https://raw.githubusercontent.com/StevenMProtech/SevenGables/main/seven%20gables.png" alt="Seven Gables Real Estate" style="width: 180px; height: auto; margin-bottom: 15px;" />
                <div class="tagline">Your Next Chapter Campaign Dashboard</div>
            </div>
            
            <div class="sidebar-stats">
                <div class="stat-card">
                <h3>Total Submissions</h3>
                <div class="number">{total}</div>
                <div class="label">All time</div>
            </div>
            
            <div class="stat-card">
                <h3>Pending Review</h3>
                <div class="number">{pending}</div>
                <div class="label">Needs follow-up</div>
            </div>
            
            <div class="stat-card">
                <h3>Maximize Priority</h3>
                <div class="number">{maximize}</div>
                <div class="label">Want $788k</div>
            </div>
            
            <div class="stat-card">
                <h3>Speed Priority</h3>
                <div class="number">{speed}</div>
                <div class="label">Quick timeline</div>
            </div>
            
            <div class="stat-card">
                <h3>Balanced</h3>
                <div class="number">{balance}</div>
                <div class="label">Both matter</div>
            </div>
            
            <div class="stat-card">
                <h3>Exploring</h3>
                <div class="number">{exploring}</div>
                <div class="label">Just curious</div>
            </div>
            </div>
            
            <div class="actions">
                <h3>Quick Actions</h3>
                <a href="/submissions" class="btn">View All Submissions</a>
                <a href="/export" class="btn secondary">Export to CSV</a>
                <a href="/api/submissions" class="btn outline">API (JSON)</a>
            </div>
        </div>
        
        <div class="preview">
            <div class="preview-header">
                <div>
                    <h2>Live Email Campaign Preview</h2>
                </div>
                <div class="zoom-controls">
                    <button class="zoom-btn" onclick="zoomOut()">−</button>
                    <span class="zoom-level" id="zoomLevel">100%</span>
                    <button class="zoom-btn" onclick="zoomIn()">+</button>
                    <div class="badge">LIVE & TESTABLE</div>
                </div>
            </div>
            <script>
                let currentZoom = 1.0;
                function zoomIn() {{
                    if (currentZoom < 1.5) {{
                        currentZoom += 0.1;
                        updateZoom();
                    }}
                }}
                function zoomOut() {{
                    if (currentZoom > 0.5) {{
                        currentZoom -= 0.1;
                        updateZoom();
                    }}
                }}
                function updateZoom() {{
                    document.querySelector('.email-container').style.zoom = currentZoom;
                    document.getElementById('zoomLevel').textContent = Math.round(currentZoom * 100) + '%';
                }}
            </script>
            <div class="email-container">
                {email_html}
            </div>
        </div>
    </div>
</body>
</html>"""

@app.route('/api/submit', methods=['POST', 'OPTIONS'])
def submit_form():
    if request.method == 'OPTIONS':
        return '', 200
    
    submissions = load_submissions()
    
    new_submission = {
        'id': len(submissions) + 1,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'email': request.form.get('email', ''),
        'first_name': request.form.get('firstName', ''),
        'last_name': request.form.get('lastName', ''),
        'equity_priority': request.form.get('equity_priority', ''),
        'goals': ','.join(request.form.getlist('goals')),
        'goals_text': request.form.get('goalsText', ''),
        'phone_number': request.form.get('phoneNumber', ''),
        'wants_equity_report': request.form.get('wantsReport') == 'yes',
        'wants_expert_contact': request.form.get('wantsExpert') == 'yes',
        'status': 'pending'
    }
    
    submissions.insert(0, new_submission)
    save_submissions(submissions)
    
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You - Seven Gables Real Estate</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            background: white;
            padding: 60px 40px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
            text-align: center;
        }
        .logo { font-size: 32px; font-weight: 700; margin-bottom: 30px; }
        .logo span { color: #d4af37; font-style: italic; }
        .checkmark {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #8b7d72 0%, #6b5d52 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 30px;
        }
        .checkmark::after {
            content: "✓";
            font-size: 48px;
            color: #d4af37;
            font-weight: bold;
        }
        h1 { color: #6b5d52; font-size: 36px; margin-bottom: 20px; }
        p { color: #d0c5b8; font-size: 18px; line-height: 1.6; margin-bottom: 15px; }
        .highlight {
            background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
            padding: 25px;
            border-radius: 12px;
            margin-top: 30px;
            border-left: 4px solid #d4af37;
        }
        .footer { margin-top: 40px; font-size: 14px; color: #e8e3dd; font-style: italic; }
        .back-btn {
            display: inline-block;
            margin-top: 30px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #d4af37 0%, #c9a22e 100%);
            color: #6b5d52;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Seven <span>Gables</span></div>
        <div class="checkmark"></div>
        <h1>Thank You!</h1>
        <p>We've received your information and are excited to reconnect with you.</p>
        <div class="highlight">
            <p style="margin: 0; color: #6b5d52; font-weight: 600;">What happens next?</p>
            <p style="margin: 10px 0 0 0; font-size: 16px;">Your dedicated Seven Gables advisor will reach out within 24 hours to discuss your home's value and explore the possibilities for your next chapter.</p>
        </div>
        <div class="footer">
            <p>49 years of Southern California expertise.<br>Independent. Forward-thinking. Built on relationships.</p>
        </div>
        <a href="/" class="back-btn">Back to Dashboard</a>
    </div>
</body>
</html>"""

@app.route('/submissions')
def submissions_page():
    submissions = load_submissions()
    
    rows = ""
    for s in submissions:
        rows += f"""
        <tr>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">{s.get('id', '')}</td>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">{s.get('timestamp', '')}</td>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">{s.get('first_name', '')} {s.get('last_name', '')}</td>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">{s.get('email', '')}</td>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">{s.get('phone_number', '')}</td>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">{s.get('equity_priority', '')}</td>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;">{s.get('goals', '')}</td>
            <td style="padding: 15px; border-bottom: 1px solid #e0e0e0;"><span style="background: #d4af37; color: #6b5d52; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">{s.get('status', 'pending')}</span></td>
        </tr>
        """
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Submissions - Seven Gables Real Estate</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f5f5f5;
            padding: 40px 20px;
        }}
        .header {{
            max-width: 1400px;
            margin: 0 auto 30px;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            font-size: 32px;
            color: #6b5d52;
            margin-bottom: 10px;
            font-family: Georgia, serif;
        }}
        .header h1 span {{ color: #d4af37; font-style: italic; }}
        .header p {{ color: #d0c5b8; }}
        .back-btn {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: linear-gradient(135deg, #d4af37 0%, #c9a22e 100%);
            color: #6b5d52;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #6b5d52;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 1px;
        }}
        td {{
            font-size: 14px;
            color: #333;
        }}
        tr:hover {{
            background: #fafafa;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Seven <span>Gables</span> Real Estate</h1>
        <p>All Submissions ({len(submissions)} total)</p>
        <a href="/" class="back-btn">← Back to Dashboard</a>
    </div>
    <div class="container">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Timestamp</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Priority</th>
                    <th>Goals</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else '<tr><td colspan="8" style="padding: 40px; text-align: center; color: #e8e3dd;">No submissions yet</td></tr>'}
            </tbody>
        </table>
    </div>
</body>
</html>"""

@app.route('/export')
def export_csv():
    submissions = load_submissions()
    
    csv_content = "ID,Timestamp,First Name,Last Name,Email,Phone,Equity Priority,Goals,Goals Text,Wants Report,Wants Expert,Status\n"
    
    for s in submissions:
        csv_content += f"{s.get('id', '')},{s.get('timestamp', '')},{s.get('first_name', '')},{s.get('last_name', '')},{s.get('email', '')},{s.get('phone_number', '')},{s.get('equity_priority', '')},\"{s.get('goals', '')}\",\"{s.get('goals_text', '')}\",{s.get('wants_equity_report', False)},{s.get('wants_expert_contact', False)},{s.get('status', '')}\n"
    
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=seven_gables_submissions.csv"}
    )

@app.route('/api/submissions')
def api_submissions():
    submissions = load_submissions()
    return jsonify(submissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

