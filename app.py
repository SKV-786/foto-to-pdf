from flask import Flask, render_template, request, send_file
from PIL import Image, UnidentifiedImageError
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')
    image_list = []

    for file in files:
        if not file or file.filename == '':
            continue  # Skip if file is empty or missing filename

        try:
            img = Image.open(file.stream).convert('RGB')

            # Optional: Resize to a reasonable A4-ish max
            max_size = (1500, 2000)
            img.thumbnail(max_size)

            image_list.append(img)
        except (UnidentifiedImageError, OSError):
            continue  # Skip invalid image files

    # ❗ If no images were valid/uploaded
    if not image_list:
        return "No valid images uploaded. Please select image files first.", 400

    # ✅ Generate PDF in memory
    pdf_buffer = BytesIO()
    image_list[0].save(
        pdf_buffer, format='PDF', save_all=True,
        append_images=image_list[1:]
    )
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name='output.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
