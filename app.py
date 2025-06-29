from flask import Flask, request, send_file, render_template_string
from PIL import Image
import io

app = Flask(__name__)

# Your full index.html file as a string (replace this with a proper file if needed)
with open("templates/index.html", encoding="utf-8") as f:
    html_template = f.read()

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')
    if not images:
        return "No images uploaded.", 400

    image_list = []

    for img in images:
        image = Image.open(img)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        max_size = 1024
        image.thumbnail((max_size, max_size), Image.LANCZOS)

        image_list.append(image)

    if not image_list:
        return "No valid images to process.", 400

    pdf_bytes = io.BytesIO()
    image_list[0].save(
        pdf_bytes,
        format='PDF',
        save_all=True,
        append_images=image_list[1:],
        quality=75,
        optimize=True
    )
    pdf_bytes.seek(0)

    return send_file(
        pdf_bytes,
        download_name='output.pdf',
        mimetype='application/pdf',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
