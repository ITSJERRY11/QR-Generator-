from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_base64 = None 

    if request.method == 'POST':
        link = request.form.get('link')

        if link:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template('index.html', qr_image=qr_base64)

if __name__ == '__main__':
    app.run(debug=True)