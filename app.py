# # from flask import Flask, render_template, request, send_from_directory, jsonify
# # import os
# #
# # app = Flask(__name__)
# #
# # # Get the path to the user's Downloads folder
# # downloads_folder = os.path.expanduser("~/Downloads")
# #
# # # Set the upload folder for temporary storage
# # UPLOAD_FOLDER = 'uploads'
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# #
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# #
# # @app.route('/')
# # def index():
# #     return render_template('index.html')
# #
# # @app.route('/upload', methods=['POST'])
# # def upload_file():
# #     if 'file' not in request.files:
# #         return jsonify({'success': False, 'error': 'No file part'})
# #
# #     file = request.files['file']
# #     if file.filename == '':
# #         return jsonify({'success': False, 'error': 'No selected file'})
# #
# #     if file and file.filename.endswith('.stp'):
# #         filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
# #         file.save(filename)
# #
# #         # Convert the .stp file to .txt and store in Downloads folder
# #         txt_filename = convert_to_txt(filename, file.filename)
# #
# #         if txt_filename:
# #             # Send the filename for download
# #             return jsonify({'success': True, 'filename': txt_filename})
# #
# #     return jsonify({'success': False, 'error': 'File not allowed. Please upload a .stp file.'})
# #
# # def convert_to_txt(stp_path, original_filename):
# #     try:
# #         # Strip the .stp extension and create the .txt file name
# #         txt_filename = original_filename.rsplit('.', 1)[0] + '.txt'
# #
# #         # Define the output .txt file path in the Downloads folder
# #         output_txt = os.path.join(downloads_folder, txt_filename)
# #
# #         # Read the content from the .stp file
# #         with open(stp_path, 'r') as stp_file:
# #             content = stp_file.read()
# #
# #         # Write the content to the .txt file in the Downloads folder
# #         with open(output_txt, 'w') as txt_file:
# #             txt_file.write(content)
# #
# #         return txt_filename
# #
# #     except Exception as e:
# #         return None
# #
# # @app.route('/download/<filename>')
# # def download_file(filename):
# #     # Send the file from the Downloads folder for download
# #     return send_from_directory(downloads_folder, filename)
# #
# # if __name__ == '__main__':
# #     app.run(debug=True)
#
#
# from flask import Flask, render_template, request, send_from_directory, jsonify
# import os
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
#
# # Path to the Downloads folder
# downloads_folder = os.path.expanduser("~/Downloads")
#
# # Upload folder for temporary storage
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'success': False, 'error': 'No file part'})
#
#     file = request.files['file']
#     filename = file.filename
#
#     if not filename:
#         return jsonify({'success': False, 'error': 'No selected file'})
#
#     # Validate file extension
#     if not filename.lower().endswith('.stp'):
#         return jsonify({'success': False, 'error': 'Invalid file extension. Please upload a .stp file.'})
#
#     # Save the uploaded file securely
#     safe_filename = secure_filename(filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
#     file.save(file_path)
#
#     # Convert the .stp file to .txt
#     txt_filename = convert_to_txt(file_path, safe_filename)
#     if txt_filename:
#         return jsonify({'success': True, 'filename': txt_filename})
#
#     return jsonify({'success': False, 'error': 'Conversion failed. Please try again.'})
#
# def convert_to_txt(stp_path, original_filename):
#     try:
#         # Strip the .stp extension to create the .txt file name
#         txt_filename = original_filename.rsplit('.', 1)[0] + '.txt'
#
#         # Define the output .txt file path in the Downloads folder
#         output_txt = os.path.join(downloads_folder, txt_filename)
#
#         # Read the content from the .stp file
#         with open(stp_path, 'r') as stp_file:
#             content = stp_file.read()
#
#         # Write the content to the .txt file in the Downloads folder
#         with open(output_txt, 'w') as txt_file:
#             txt_file.write(content)
#
#         return txt_filename
#     except Exception as e:
#         print(f"Error during conversion: {e}")
#         return None
#
# @app.route('/download/<filename>')
# def download_file(filename):
#     # Send the file from the Downloads folder for download
#     return send_from_directory(downloads_folder, filename)
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Path to store uploaded files and temporary converted files
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Configure the app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

@app.route('/')
def index():
    # Render the HTML page
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['file']
    filename = file.filename

    if not filename:
        return jsonify({'success': False, 'error': 'No selected file'})

    # Validate file extension
    if not filename.lower().endswith('.stp'):
        return jsonify({'success': False, 'error': 'Invalid file extension. Please upload a .stp file.'})

    # Save the uploaded file
    safe_filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(file_path)

    # Convert the .stp file to .txt
    txt_filename = convert_to_txt(file_path, safe_filename)
    if txt_filename:
        return jsonify({'success': True, 'filename': txt_filename})

    return jsonify({'success': False, 'error': 'Conversion failed. Please try again.'})

def convert_to_txt(stp_path, original_filename):
    """
    Converts an .stp file to a .txt file by copying its content.
    Stores the .txt file in the CONVERTED_FOLDER.
    """
    try:
        # Strip the .stp extension and create the .txt file name
        txt_filename = original_filename.rsplit('.', 1)[0] + '.txt'

        # Define the output .txt file path in the converted folder
        output_txt = os.path.join(app.config['CONVERTED_FOLDER'], txt_filename)

        # Read the content from the .stp file
        with open(stp_path, 'r') as stp_file:
            content = stp_file.read()

        # Write the content to the .txt file in the converted folder
        with open(output_txt, 'w') as txt_file:
            txt_file.write(content)

        return txt_filename

    except Exception as e:
        print(f"Error during conversion: {e}")
        return None

@app.route('/download/<filename>')
def download_file(filename):
    """
    Serves the converted .txt file for download from the CONVERTED_FOLDER.
    """
    file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['CONVERTED_FOLDER'], filename, as_attachment=True)
    return jsonify({'success': False, 'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
