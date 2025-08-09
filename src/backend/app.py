#!/usr/bin/env python3
"""
Flask Backend for PDF Tools - Azure App Service Ready
Tools: DOCX to PDF, PDF to DOCX, PDF Compression
Features: File caching, efficient processing, CORS support, Azure optimization
"""

import os
import tempfile
import subprocess
import hashlib
import logging
from datetime import datetime
from pathlib import Path
import zipfile
import shutil

from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# PDF and document processing libraries
try:
    from pdf2docx import Converter
    PDF2DOCX_AVAILABLE = True
except ImportError:
    PDF2DOCX_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Azure-optimized CORS configuration
CORS(app, origins=[
    "https://techuhat.github.io",
    "https://image2.vercel.app", 
    "http://localhost:3000",
    "http://127.0.0.1:3000"
])

# Azure-compatible logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Azure uses stdout for logging
    ]
)
logger = logging.getLogger(__name__)

# Create directories for caching
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def get_file_hash(file_content):
    """Generate SHA256 hash of file content for caching"""
    return hashlib.sha256(file_content).hexdigest()

def check_ghostscript():
    """Check if Ghostscript is available in system"""
    try:
        result = subprocess.run(['gs', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

# System capability checks
GHOSTSCRIPT_AVAILABLE = check_ghostscript()

@app.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint"""
    return "pong"

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    """Comprehensive health check with system capabilities"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "message": "Backend ready for PDF and Image processing",
        "capabilities": {
            "pdf_compression": GHOSTSCRIPT_AVAILABLE or PYMUPDF_AVAILABLE,
            "pdf_to_docx": PDF2DOCX_AVAILABLE or PYMUPDF_AVAILABLE,
            "image_compression": True,  # Always available with Pillow
            "batch_processing": True
        },
        "system_tools": {
            "ghostscript": GHOSTSCRIPT_AVAILABLE,
            "pdf2docx": PDF2DOCX_AVAILABLE,
            "pymupdf": PYMUPDF_AVAILABLE,
            "pillow": True
        },
        "supported_operations": [
            "compress-pdf",
            "pdf-to-docx", 
            "compress-image",
            "batch-process"
        ],
        "limits": {
            "max_file_size": "100MB",
            "max_batch_files": 10,
            "supported_formats": {
                "pdf": ["pdf"],
                "image": ["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
                "document": ["docx"]
            }
        }
    })

@app.route('/pdf-to-docx', methods=['POST'])
def pdf_to_docx():
    """
    Convert PDF to DOCX using pdf2docx or PyMuPDF
    Features: File caching, multiple conversion methods
    """
    logger.info("PDF to DOCX conversion request received")
    
    if not (PDF2DOCX_AVAILABLE or PYMUPDF_AVAILABLE):
        return jsonify({
            "error": "PDF to DOCX conversion not available. Install pdf2docx or PyMuPDF"
        }), 500
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    force_conversion = request.form.get('force', 'false').lower() == 'true'
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400
    
    try:
        # Read file content and generate hash
        file_content = file.read()
        file_hash = get_file_hash(file_content)
        
        # Generate filenames
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        output_filename = f"{base_name}.docx"
        
        # Check cache
        cached_file = CACHE_DIR / f"{file_hash}_{output_filename}"
        
        if cached_file.exists() and not force_conversion:
            logger.info(f"Returning cached DOCX: {output_filename}")
            return send_file(
                cached_file,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        
        # Create temporary files
        temp_pdf = TEMP_DIR / f"{file_hash}_input.pdf"
        temp_docx = TEMP_DIR / f"{file_hash}_output.docx"
        
        # Write PDF file
        with open(temp_pdf, 'wb') as f:
            f.write(file_content)
        
        conversion_success = False
        conversion_method = ""
        
        # Method 1: Try pdf2docx (most accurate)
        if PDF2DOCX_AVAILABLE and not conversion_success:
            try:
                logger.info("Attempting conversion with pdf2docx")
                converter = Converter(str(temp_pdf))
                converter.convert(str(temp_docx))
                converter.close()
                conversion_success = True
                conversion_method = "pdf2docx"
                logger.info("Conversion successful with pdf2docx")
            except Exception as e:
                logger.warning(f"pdf2docx conversion failed: {e}")
        
        # Method 2: Try PyMuPDF (fallback)
        if PYMUPDF_AVAILABLE and not conversion_success:
            try:
                logger.info("Attempting conversion with PyMuPDF")
                import docx
                
                doc = fitz.open(str(temp_pdf))
                word_doc = docx.Document()
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    
                    if text.strip():
                        word_doc.add_paragraph(text)
                        if page_num < len(doc) - 1:
                            word_doc.add_page_break()
                
                doc.close()
                word_doc.save(str(temp_docx))
                conversion_success = True
                conversion_method = "pymupdf"
                logger.info("Conversion successful with PyMuPDF")
                
            except Exception as e:
                logger.warning(f"PyMuPDF conversion failed: {e}")
        
        if not conversion_success:
            return jsonify({
                "error": "All conversion methods failed",
                "details": "PDF may be corrupted, password-protected, or contain unsupported content"
            }), 500
        
        # Copy to cache
        shutil.copy2(temp_docx, cached_file)
        
        # Log conversion
        logger.info(f"Successfully converted {original_name} to DOCX using {conversion_method}")
        
        @after_this_request
        def cleanup(response):
            try:
                if temp_pdf.exists():
                    temp_pdf.unlink()
                if temp_docx.exists():
                    temp_docx.unlink()
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")
            return response
        
        return send_file(
            cached_file,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        logger.error(f"PDF to DOCX conversion error: {str(e)}")
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    """
    Compress PDF using Ghostscript or PyMuPDF
    Features: Size optimization, quality control, smart caching
    """
    logger.info("PDF compression request received")
    
    if not (GHOSTSCRIPT_AVAILABLE or PYMUPDF_AVAILABLE):
        return jsonify({
            "error": "PDF compression not available. Install Ghostscript or PyMuPDF"
        }), 500
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    force_compression = request.form.get('force', 'false').lower() == 'true'
    
    # Quality settings for Ghostscript
    quality_map = {
        'low': '/screen',      # Lowest quality, smallest size
        'medium': '/ebook',    # Medium quality
        'high': '/printer',    # High quality
        'max': '/prepress'     # Maximum quality
    }
    quality = request.form.get('quality', 'medium').lower()
    gs_quality = quality_map.get(quality, '/ebook')
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400
    
    try:
        # Read file content and generate hash
        file_content = file.read()
        file_hash = get_file_hash(file_content)
        original_size = len(file_content)
        
        # Generate filenames
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        output_filename = f"{base_name}_compressed.pdf"
        
        # Check cache with quality suffix
        cached_file = CACHE_DIR / f"{file_hash}_{quality}_{output_filename}"
        
        if cached_file.exists() and not force_compression:
            compressed_size = cached_file.stat().st_size
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            logger.info(f"Returning cached compressed PDF: {output_filename} ({compression_ratio:.1f}% reduction)")
            
            response = send_file(
                cached_file,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/pdf'
            )
            response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
            response.headers['X-Original-Size'] = str(original_size)
            response.headers['X-Compressed-Size'] = str(compressed_size)
            return response
        
        # Check if file is already small enough
        if original_size < 1024 * 1024 and not force_compression:  # < 1MB
            logger.info("File already small, skipping compression")
            response = send_file(
                file_content,
                as_attachment=True,
                download_name=original_name,
                mimetype='application/pdf'
            )
            response.headers['X-Compression-Ratio'] = "0%"
            response.headers['X-Message'] = "File already optimized"
            return response
        
        # Create temporary files
        temp_input = TEMP_DIR / f"{file_hash}_input.pdf"
        temp_output = TEMP_DIR / f"{file_hash}_compressed.pdf"
        
        # Write input file
        with open(temp_input, 'wb') as f:
            f.write(file_content)
        
        compression_success = False
        compression_method = ""
        
        # Method 1: Try Ghostscript (preferred for compression)
        if GHOSTSCRIPT_AVAILABLE and not compression_success:
            try:
                logger.info(f"Attempting compression with Ghostscript (quality: {quality})")
                
                cmd = [
                    'gs',
                    '-sDEVICE=pdfwrite',
                    '-dCompatibilityLevel=1.4',
                    f'-dPDFSETTINGS={gs_quality}',
                    '-dNOPAUSE',
                    '-dQUIET',
                    '-dBATCH',
                    f'-sOutputFile={temp_output}',
                    str(temp_input)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0 and temp_output.exists():
                    compression_success = True
                    compression_method = "ghostscript"
                    logger.info("Compression successful with Ghostscript")
                else:
                    logger.warning(f"Ghostscript compression failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.warning("Ghostscript compression timeout")
            except Exception as e:
                logger.warning(f"Ghostscript compression error: {e}")
        
        # Method 2: Try PyMuPDF (fallback)
        if PYMUPDF_AVAILABLE and not compression_success:
            try:
                logger.info("Attempting compression with PyMuPDF")
                
                doc = fitz.open(str(temp_input))
                
                # Compression options based on quality
                deflate_level = {
                    'low': 9,
                    'medium': 6,
                    'high': 3,
                    'max': 1
                }.get(quality, 6)
                
                doc.save(
                    str(temp_output),
                    garbage=4,
                    deflate=True,
                    deflate_images=True,
                    deflate_fonts=True,
                    linear=True,
                    clean=True,
                    pretty=False,
                    ascii=False,
                    expand=0,
                    compression=deflate_level
                )
                
                doc.close()
                compression_success = True
                compression_method = "pymupdf"
                logger.info("Compression successful with PyMuPDF")
                
            except Exception as e:
                logger.warning(f"PyMuPDF compression error: {e}")
        
        if not compression_success:
            return jsonify({
                "error": "All compression methods failed",
                "details": "PDF may be corrupted or already optimized"
            }), 500
        
        # Calculate compression ratio
        compressed_size = temp_output.stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        # Only keep compressed version if it's actually smaller
        if compressed_size >= original_size and not force_compression:
            logger.info("Compression didn't reduce file size, returning original")
            response = send_file(
                temp_input,
                as_attachment=True,
                download_name=original_name,
                mimetype='application/pdf'
            )
            response.headers['X-Compression-Ratio'] = "0%"
            response.headers['X-Message'] = "Original file already optimized"
            return response
        
        # Copy to cache
        shutil.copy2(temp_output, cached_file)
        
        # Log compression
        logger.info(f"Successfully compressed {original_name} using {compression_method} "
                   f"({compression_ratio:.1f}% reduction: {original_size} -> {compressed_size} bytes)")
        
        @after_this_request
        def cleanup(response):
            try:
                if temp_input.exists():
                    temp_input.unlink()
                if temp_output.exists():
                    temp_output.unlink()
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")
            return response
        
        response = send_file(
            cached_file,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
        response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
        response.headers['X-Original-Size'] = str(original_size)
        response.headers['X-Compressed-Size'] = str(compressed_size)
        response.headers['X-Method'] = compression_method
        
        return response
        
    except Exception as e:
        logger.error(f"PDF compression error: {str(e)}")
        return jsonify({"error": f"Compression failed: {str(e)}"}), 500

@app.route('/compress-image', methods=['POST'])
def compress_image():
    """
    Compress image files using Pillow
    Features: Quality control, format optimization, smart caching
    """
    logger.info("Image compression request received")
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    quality = int(request.form.get('quality', 85))  # Default quality 85%
    force_compression = request.form.get('force', 'false').lower() == 'true'
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Supported image formats
    supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in supported_formats:
        return jsonify({"error": f"Unsupported format. Supported: {', '.join(supported_formats)}"}), 400
    
    try:
        from PIL import Image
        import io
        
        # Read file content and generate hash
        file_content = file.read()
        file_hash = get_file_hash(file_content)
        original_size = len(file_content)
        
        # Generate filenames
        original_name = secure_filename(file.filename)
        base_name = Path(original_name).stem
        output_filename = f"{base_name}_compressed{file_ext}"
        
        # Check cache with quality suffix
        cached_file = CACHE_DIR / f"{file_hash}_q{quality}_{output_filename}"
        
        if cached_file.exists() and not force_compression:
            compressed_size = cached_file.stat().st_size
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            logger.info(f"Returning cached compressed image: {output_filename} ({compression_ratio:.1f}% reduction)")
            
            response = send_file(
                cached_file,
                as_attachment=True,
                download_name=output_filename,
                mimetype=f'image/{file_ext[1:]}'
            )
            response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
            response.headers['X-Original-Size'] = str(original_size)
            response.headers['X-Compressed-Size'] = str(compressed_size)
            return response
        
        # Open and process image
        img = Image.open(io.BytesIO(file_content))
        
        # Convert RGBA to RGB if saving as JPEG
        if file_ext.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparency
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Compress and save
        output_buffer = io.BytesIO()
        
        save_kwargs = {
            'format': img.format if img.format else 'JPEG',
            'quality': quality,
            'optimize': True
        }
        
        # Format specific optimizations
        if file_ext.lower() in ['.jpg', '.jpeg']:
            save_kwargs['progressive'] = True
        elif file_ext.lower() == '.png':
            save_kwargs['compress_level'] = 9
            del save_kwargs['quality']  # PNG doesn't use quality
        elif file_ext.lower() == '.webp':
            save_kwargs['method'] = 6  # Better compression
        
        img.save(output_buffer, **save_kwargs)
        compressed_data = output_buffer.getvalue()
        compressed_size = len(compressed_data)
        
        # Calculate compression ratio
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        # Only keep compressed version if it's actually smaller
        if compressed_size >= original_size and not force_compression:
            logger.info("Compression didn't reduce file size, returning original")
            response = send_file(
                io.BytesIO(file_content),
                as_attachment=True,
                download_name=original_name,
                mimetype=f'image/{file_ext[1:]}'
            )
            response.headers['X-Compression-Ratio'] = "0%"
            response.headers['X-Message'] = "Original file already optimized"
            return response
        
        # Save to cache
        with open(cached_file, 'wb') as f:
            f.write(compressed_data)
        
        # Log compression
        logger.info(f"Successfully compressed {original_name} "
                   f"({compression_ratio:.1f}% reduction: {original_size} -> {compressed_size} bytes)")
        
        response = send_file(
            io.BytesIO(compressed_data),
            as_attachment=True,
            download_name=output_filename,
            mimetype=f'image/{file_ext[1:]}'
        )
        response.headers['X-Compression-Ratio'] = f"{compression_ratio:.1f}%"
        response.headers['X-Original-Size'] = str(original_size)
        response.headers['X-Compressed-Size'] = str(compressed_size)
        
        return response
        
    except Exception as e:
        logger.error(f"Image compression error: {str(e)}")
        return jsonify({"error": f"Compression failed: {str(e)}"}), 500

@app.route('/batch-process', methods=['POST'])
def batch_process():
    """
    Batch process multiple files
    Supports mixed operations and returns ZIP archive
    """
    logger.info("Batch processing request received")
    
    if 'files' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    
    files = request.files.getlist('files')
    operation = request.form.get('operation', 'auto')  # auto, compress, convert
    
    if len(files) > 10:
        return jsonify({"error": "Maximum 10 files allowed in batch"}), 400
    
    if not files or all(f.filename == '' for f in files):
        return jsonify({"error": "No files selected"}), 400
    
    try:
        # Create temporary directory for batch processing
        batch_id = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]
        batch_dir = TEMP_DIR / f"batch_{batch_id}"
        batch_dir.mkdir(exist_ok=True)
        
        processed_files = []
        errors = []
        
        for file in files:
            if file.filename == '':
                continue
                
            try:
                original_name = secure_filename(file.filename)
                file_ext = Path(original_name).suffix.lower()
                
                # Determine operation based on file type and user preference
                if operation == 'auto':
                    if file_ext == '.pdf':
                        # Auto: compress PDF
                        current_op = 'compress'
                    elif file_ext == '.docx':
                        # Auto: convert DOCX to PDF
                        current_op = 'convert_to_pdf'
                    else:
                        errors.append(f"{original_name}: Unsupported file type")
                        continue
                else:
                    current_op = operation
                
                # Process file based on operation
                if current_op == 'compress' and file_ext == '.pdf':
                    # Simulate compression endpoint logic
                    file_content = file.read()
                    temp_file = batch_dir / f"compressed_{original_name}"
                    
                    # For batch, use simple PyMuPDF compression
                    if PYMUPDF_AVAILABLE:
                        temp_input = batch_dir / f"input_{original_name}"
                        with open(temp_input, 'wb') as f:
                            f.write(file_content)
                        
                        doc = fitz.open(str(temp_input))
                        doc.save(str(temp_file), garbage=4, deflate=True)
                        doc.close()
                        
                        processed_files.append(str(temp_file))
                    else:
                        errors.append(f"{original_name}: Compression not available")
                
                elif current_op == 'convert_to_pdf' and file_ext == '.docx':
                    # Simulate DOCX to PDF conversion
                    if LIBREOFFICE_AVAILABLE:
                        file_content = file.read()
                        temp_input = batch_dir / original_name
                        
                        with open(temp_input, 'wb') as f:
                            f.write(file_content)
                        
                        cmd = [
                            'libreoffice',
                            '--headless',
                            '--convert-to', 'pdf',
                            '--outdir', str(batch_dir),
                            str(temp_input)
                        ]
                        
                        result = subprocess.run(cmd, capture_output=True, timeout=60)
                        
                        if result.returncode == 0:
                            pdf_name = Path(original_name).stem + '.pdf'
                            pdf_file = batch_dir / pdf_name
                            if pdf_file.exists():
                                processed_files.append(str(pdf_file))
                            else:
                                errors.append(f"{original_name}: PDF not generated")
                        else:
                            errors.append(f"{original_name}: Conversion failed")
                    else:
                        errors.append(f"{original_name}: LibreOffice not available")
                
                else:
                    errors.append(f"{original_name}: Operation not supported for this file type")
                    
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")
        
        if not processed_files:
            return jsonify({
                "error": "No files were successfully processed",
                "errors": errors
            }), 400
        
        # Create ZIP archive
        zip_filename = f"batch_processed_{batch_id}.zip"
        zip_path = batch_dir / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in processed_files:
                file_path_obj = Path(file_path)
                zipf.write(file_path, file_path_obj.name)
        
        logger.info(f"Batch processing completed: {len(processed_files)} files processed, {len(errors)} errors")
        
        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(batch_dir)
            except Exception as e:
                logger.warning(f"Batch cleanup error: {e}")
            return response
        
        response = send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        response.headers['X-Processed-Files'] = str(len(processed_files))
        response.headers['X-Errors'] = str(len(errors))
        
        return response
        
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        return jsonify({"error": f"Batch processing failed: {str(e)}"}), 500

@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    """Clear the cache directory"""
    try:
        cache_files = list(CACHE_DIR.glob('*'))
        temp_files = list(TEMP_DIR.glob('*'))
        
        for file_path in cache_files + temp_files:
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)
        
        logger.info(f"Cache cleared: {len(cache_files)} cache files, {len(temp_files)} temp files")
        
        return jsonify({
            "message": "Cache cleared successfully",
            "files_removed": len(cache_files) + len(temp_files)
        })
        
    except Exception as e:
        logger.error(f"Cache clear error: {str(e)}")
        return jsonify({"error": f"Cache clear failed: {str(e)}"}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 100MB"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
