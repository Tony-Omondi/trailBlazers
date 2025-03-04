from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime

def send_account_activation_email(email, email_token):
    subject = "Activate Your Account"
    email_from = settings.DEFAULT_FROM_EMAIL
    activation_link = f'http:shujaacreatives/accounts/activate/{email_token}'
    current_year = datetime.now().year
    
    # HTML content for the email
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        /* General Styles */
        body {{
            font-family: 'Poppins', Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .email-container {{
            max-width: 750px;
            margin: 20px auto;
            background: #ffffff;
            border-radius: 15px;
            box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 32px;
            margin: 0;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .header img {{
            width: 80px;
            height: auto;
            margin-top: 10px;
        }}
        .content {{
            padding: 20px 30px;
            text-align: center;
        }}
        .content h2 {{
            font-size: 24px;
            color: #111;
            margin-bottom: 20px;
        }}
        .content p {{
            font-size: 16px;
            color: #555;
            margin-bottom: 20px;
            line-height: 1.8;
        }}
        .cta {{
            margin-top: 20px;
        }}
        .cta a {{
            display: inline-block;
            background: linear-gradient(90deg, #ff6a00, #ee0979);
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 50px;
            transition: all 0.3s ease;
        }}
        .cta a:hover {{
            transform: translateY(-5px);
            box-shadow: 0px 5px 15px rgba(255, 105, 135, 0.6);
        }}
        .social-icons {{
            margin-top: 20px;
            text-align: center;
        }}
        .social-icons a {{
            margin: 0 10px;
            display: inline-block;
            text-decoration: none;
        }}
        .social-icons img {{
            width: 32px;
            height: 32px;
            transition: transform 0.3s ease;
        }}
        .social-icons img:hover {{
            transform: scale(1.2);
        }}
        .footer {{
            background: #f7f7f7;
            padding: 20px 30px;
            text-align: center;
            font-size: 14px;
            color: #555;
            border-top: 1px solid #ddd;
        }}
        .footer a {{
            color: #ff6a00;
            text-decoration: none;
            font-weight: bold;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header">
            <h1>Welcome to ShopNow!</h1>
            <img src="https://your-logo-url.com/logo.png" alt="ShopNow Logo">
        </div>
        
        <!-- Content -->
        <div class="content">
            <h2>Activate Your Account & Start Shopping!</h2>
            <p>Thank you for joining ShopNow, where you’ll find the best deals, exclusive offers, and trending products!</p>
            <p>To access your account and explore our amazing catalog, please activate your account by clicking below:</p>
            <div class="cta">
                <a href="{activation_link}">Activate My Account</a>
            </div>
        </div>

        <!-- Social Media -->
        <div class="social-icons">
            <a href="https://www.tiktok.com" target="_blank">
                <img src="./tiktok-icon.svg" alt="TikTok">
            </a>
            <a href="https://www.instagram.com" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram">
            </a>
            <a href="https://wa.me/your_number" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
            </a>
            <a href="https://www.x.com" target="_blank">
                <img src="./x-social-media-logo-icon.svg" alt="X">
            </a>
            <a href="https://www.facebook.com" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook">
            </a>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>&copy; {current_year} ShopNow. All rights reserved.</p>
            <p><a href="#">Terms of Service</a> | <a href="#">Privacy Policy</a></p>
        </div>
    </div>
</body>
</html>
"""

    
    # Send email
    email_message = EmailMessage(subject, html_content, email_from, [email])
    email_message.content_subtype = 'html'  # Set the email content type to HTML
    email_message.send()
