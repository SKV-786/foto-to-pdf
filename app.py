from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')
    if not images:
        return "No images uploaded.", 400

    image_list = []

    for img in images:
        image = Image.open(img)

        # Convert to RGB (removes alpha, required for PDF)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize if too large (max width or height = 1600px)
        max_size = 1600
        image.thumbnail((max_size, max_size), Image.LANCZOS)

        image_list.append(image)

    if not image_list:
        return "No valid images to process.", 400

    # Save all to one PDF in-memory
    pdf_bytes = io.BytesIO()
    image_list[0].save(
        pdf_bytes,
        format='PDF',
        save_all=True,
        append_images=image_list[1:],
        quality=75,          # Balanced for speed & quality
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
