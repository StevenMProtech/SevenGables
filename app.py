from flask import Flask, request, jsonify, send_file
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
    
    # Count goals
    goals_count = {}
    for s in submissions:
        goals = s.get('goals', [])
        if isinstance(goals, str):
            goals = [goals]
        for goal in goals:
            goals_count[goal] = goals_count.get(goal, 0) + 1
    
    # Count followup preferences
    followup_count = {}
    for s in submissions:
        followup = s.get('followup', [])
        if isinstance(followup, str):
            followup = [followup]
        for f in followup:
            followup_count[f] = followup_count.get(f, 0) + 1
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Seven Gables Campaign Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            background: #f8f6f3;
            min-height: 100vh;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(rgba(26,22,20,0.95), rgba(26,22,20,0.95)), 
                        url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200') center/cover;
            padding: 40px 30px;
            text-align: center;
            border-bottom: 3px solid #1a1614;
        }}
        .logo {{
            width: 180px;
            height: auto;
            margin-bottom: 20px;
        }}
        .header h1 {{
            color: white;
            font-size: 32px;
            font-weight: 300;
            font-style: italic;
            margin-bottom: 8px;
        }}
        .header p {{
            color: rgba(255,255,255,0.8);
            font-size: 15px;
            font-weight: 300;
        }}
        
        /* Container */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            border: 1px solid #e0ddd8;
            box-shadow: 0 2px 8px rgba(26,22,20,0.08);
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
            font-weight: 300;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .stat-value {{
            color: #1a1614;
            font-size: 42px;
            font-weight: 400;
        }}
        
        /* Submissions Table */
        .table-container {{
            background: white;
            border-radius: 8px;
            border: 1px solid #e0ddd8;
            box-shadow: 0 2px 8px rgba(26,22,20,0.08);
            overflow: hidden;
            margin-bottom: 30px;
        }}
        .table-header {{
            background: #1a1614;
            color: white;
            padding: 25px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        .table-header h2 {{
            font-size: 22px;
            font-weight: 400;
        }}
        .export-btn {{
            background: white;
            color: #1a1614;
            border: none;
            padding: 12px 24px;
            border-radius: 4px;
            cursor: pointer;
            font-family: Georgia, serif;
            font-size: 14px;
            font-weight: 400;
            text-decoration: none;
            display: inline-block;
            transition: all 0.2s;
        }}
        .export-btn:hover {{
            background: #f8f6f3;
        }}
        .table-wrapper {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #fafaf8;
            color: #1a1614;
            font-weight: 400;
            text-align: left;
            padding: 18px 20px;
            font-size: 14px;
            border-bottom: 2px solid #e0ddd8;
            white-space: nowrap;
        }}
        td {{
            padding: 18px 20px;
            border-bottom: 1px solid #f0ede8;
            color: #333;
            font-size: 14px;
            font-weight: 300;
        }}
        tr:hover {{
            background: #fafaf8;
        }}
        .email-cell {{
            color: #1a1614;
            font-weight: 400;
        }}
        .goals-cell {{
            max-width: 300px;
            line-height: 1.6;
        }}
        .timestamp {{
            color: #666;
            font-size: 13px;
        }}
        
        /* Mobile Responsive */
        @media (max-width: 768px) {{
            .header {{
                padding: 30px 20px;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .logo {{
                width: 140px;
            }}
            .container {{
                padding: 30px 15px;
            }}
            .stats-grid {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            .stat-card {{
                padding: 25px;
            }}
            .stat-value {{
                font-size: 36px;
            }}
            .table-header {{
                padding: 20px;
            }}
            .table-header h2 {{
                font-size: 18px;
            }}
            th, td {{
                padding: 12px 15px;
                font-size: 13px;
            }}
        }}
        
        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 60px 30px;
            color: #666;
        }}
        .empty-state p {{
            font-size: 16px;
            font-weight: 300;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <img src="https://raw.githubusercontent.com/StevenMProtech/SevenGables/main/seven%20gables.png" alt="Seven Gables" class="logo">
        <h1>Past Client Campaign Dashboard</h1>
        <p>Track engagement and responses from your equity campaign</p>
    </div>
    
    <!-- Container -->
    <div class="container">
        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Submissions</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Want Follow-up</div>
                <div class="stat-value">{followup_count.get('create_plan', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Relocating</div>
                <div class="stat-value">{goals_count.get('relocate', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Buy Before Sell</div>
                <div class="stat-value">{goals_count.get('buy_before_sell', 0)}</div>
            </div>
        </div>
        
        <!-- Submissions Table -->
        <div class="table-container">
            <div class="table-header">
                <h2>Recent Submissions</h2>
                <a href="/export" class="export-btn">Export to CSV</a>
            </div>
            <div class="table-wrapper">
                {"<table>" if total > 0 else ""}
                    {"<thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Goals</th><th>Location Interest</th><th>Follow-up</th><th>Submitted</th></tr></thead>" if total > 0 else ""}
                    {"<tbody>" if total > 0 else ""}
                        {''.join([f"""
                        <tr>
                            <td>{s.get('firstName', '')} {s.get('lastName', '')}</td>
                            <td class="email-cell">{s.get('email', '')}</td>
                            <td>{s.get('phone', 'N/A')}</td>
                            <td class="goals-cell">{', '.join(s.get('goals', [])) if isinstance(s.get('goals'), list) else s.get('goals', 'N/A')}</td>
                            <td>{s.get('move_details', 'N/A')}</td>
                            <td>{'Yes' if 'create_plan' in (s.get('followup', []) if isinstance(s.get('followup'), list) else [s.get('followup', '')]) else 'No'}</td>
                            <td class="timestamp">{s.get('timestamp', 'N/A')}</td>
                        </tr>
                        """ for s in reversed(submissions)])}
                    {"</tbody>" if total > 0 else ""}
                {"</table>" if total > 0 else "<div class='empty-state'><p>No submissions yet. Share your campaign to start collecting responses.</p></div>"}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/api/submit', methods=['POST'])
def submit():
    try:
        data = request.form.to_dict(flat=False)
        
        # Process form data
        submission = {{
            'email': data.get('email', [''])[0],
            'firstName': data.get('firstName', [''])[0],
            'lastName': data.get('lastName', [''])[0],
            'phone': data.get('phone', [''])[0],
            'goals': data.get('goals', []),
            'move_details': data.get('move_details', [''])[0],
            'followup': data.get('followup', []),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}
        
        submissions = load_submissions()
        submissions.append(submission)
        save_submissions(submissions)
        
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Thank You - Seven Gables</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: Georgia, 'Times New Roman', serif;
                    background: linear-gradient(rgba(26,22,20,0.95), rgba(26,22,20,0.95)), 
                                url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200') center/cover;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    max-width: 600px;
                    width: 100%;
                    padding: 60px 40px;
                    text-align: center;
                    border-radius: 8px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                }}
                .logo {{
                    width: 160px;
                    margin-bottom: 30px;
                }}
                h1 {{
                    color: #1a1614;
                    font-size: 36px;
                    font-weight: 300;
                    margin-bottom: 20px;
                }}
                p {{
                    color: #666;
                    font-size: 18px;
                    line-height: 1.7;
                    font-weight: 300;
                    margin-bottom: 15px;
                }}
                .highlight {{
                    color: #1a1614;
                    font-weight: 400;
                }}
                @media (max-width: 600px) {{
                    .container {{
                        padding: 40px 30px;
                    }}
                    h1 {{
                        font-size: 28px;
                    }}
                    p {{
                        font-size: 16px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <img src="https://raw.githubusercontent.com/StevenMProtech/SevenGables/main/seven%20gables.png" alt="Seven Gables" class="logo">
                <h1>Thank You!</h1>
                <p>We've received your information.</p>
                <p class="highlight">Michelle will reach out within 24 hours with your custom plan.</p>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

@app.route('/export')
def export():
    submissions = load_submissions()
    
    csv_content = "Name,Email,Phone,Goals,Location Interest,Follow-up,Timestamp\\n"
    for s in submissions:
        name = f"{{s.get('firstName', '')}} {{s.get('lastName', '')}}"
        email = s.get('email', '')
        phone = s.get('phone', 'N/A')
        goals = ', '.join(s.get('goals', [])) if isinstance(s.get('goals'), list) else s.get('goals', 'N/A')
        move_details = s.get('move_details', 'N/A')
        followup = 'Yes' if 'create_plan' in (s.get('followup', []) if isinstance(s.get('followup'), list) else [s.get('followup', '')]) else 'No'
        timestamp = s.get('timestamp', 'N/A')
        
        csv_content += f'"{{name}}","{{email}}","{{phone}}","{{goals}}","{{move_details}}","{{followup}}","{{timestamp}}"\\n'
    
    with open('submissions.csv', 'w') as f:
        f.write(csv_content)
    
    return send_file('submissions.csv', as_attachment=True, download_name='seven_gables_submissions.csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

