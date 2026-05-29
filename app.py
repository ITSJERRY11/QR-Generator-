import io
import base64
from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_base64 = None
    user_url = None

    if request.method == "POST":
        user_url = request.form.get("url")
        
        if user_url:
            # Configure the QR code look and feel
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(user_url)
            qr.make(fit=True)

            # Create the image (using a sleek dark blue/black color for a modern look)
            img = qr.make_image(fill_color="#1e293b", back_color="white")

            # Save the image to a memory buffer instead of disk
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Encode the image to base64 string to embed directly in HTML
            qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template("index.html", qr_base64=qr_base64, url=user_url)

if __name__ == "__main__":
    app.run(debug=True)
