from flask import Flask, render_template_string, request, send_file
import qrcode
import io
import base64

app = Flask(__name__)

# Plantilla HTML con Bootstrap
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Generador de QR</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="shortcut icon" href="https://prueba.uncuyo.edu.ar/modular_4/favicon.ico">
</head>
<style>
    body {
        background-color: #e7f2ff;
    }
    .btn-generar {
        background-color: #067CB2;
        color: white;
        font-weight: 600;
    }
    .btn-generar:hover {
        background-color: #0994d3;
        color: black;
    }
</style>
<body class="d-flex flex-column align-self-center">
    <div class="container text-center mt-5">
        <img src="{{ url_for('static', filename='encabezado.png') }}" alt="encabezado" style="max-width:80%;">
    </div>
    <div class="container text-center mt-5">
        <div class="card shadow p-4" style="border-radius: 15px;">
            <h1 class="mb-4">ASSA - SV</h1>
            <h3 class="mb-3">Generador de QR</h3>
            <form method="POST" class="mb-3">
                <div class="input-group">
                    <input type="text" name="url" placeholder="Pegá tu URL aquí" class="form-control" required>
                    <button type="submit" class="btn btn-generar">Generar</button>
                </div>
            </form>

            {% if qr %}
                <div class="mt-4">
                    <h4>✅ QR generado:</h4>
                    <img src="data:image/png;base64,{{qr}}" alt="QR Code" class="img-thumbnail mt-3" style="max-width:250px;">
                    <div class="mt-3">
                        <a href="/download?url={{url}}" class="btn btn-success">Descargar PNG</a>
                    </div>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    qr_b64 = None
    url = None
    if request.method == "POST":
        url = request.form["url"]
        # Generar QR
        img = qrcode.make(url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template_string(HTML, qr=qr_b64, url=url)


@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return "Falta la URL", 400
    
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="qr.png",
        mimetype="image/png"
    )


if __name__ == "__main__":
    app.run(debug=True)
