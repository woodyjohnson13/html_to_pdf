from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)



@app.route('/hello', methods=['POST'])
def hello():
    return "Hello World!"

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        url = data.get('url')
        
        # Path to the output PDF file
        output_pdf_path = "invoices/invoice.pdf"
        screenshot_path = "screenshots/screenshot.png"
        rotated_screenshot_path = "screenshots/rotated_screenshot.png"

        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Open the webpage
        driver.get(url)

        # Adjust the window size to match the content (optional)
        driver.set_window_size(850, driver.execute_script("return document.body.scrollHeight"))

        # Save the webpage as a screenshot
        driver.save_screenshot(screenshot_path)

        # Clean up
        driver.quit()

        print("Screenshot saved")

        # Open the screenshot using PIL
        image = Image.open(screenshot_path)

        # Rotate the image by 90 degrees clockwise
        rotated_image = image.rotate(-90, expand=True)

        # Save the rotated image
        rotated_image.save(rotated_screenshot_path)

        # Convert the rotated screenshot to PDF using fpdf
        pdf = FPDF()
        pdf.add_page()
        pdf.image(rotated_screenshot_path, 0, 0, 210, 0)  # Adjust the dimensions as needed
        pdf.output(output_pdf_path, "F")

        print("PDF saved at:", output_pdf_path)
        
        pdf_url = f"http://localhost:5000/{output_pdf_path}"  # Update the URL accordingly


        response = {
            "message": "PDF generated successfully",
            "pdf_link": pdf_url
        }

        return jsonify(response), 200

    except Exception as e:
        response = {
            "message": "Error generating PDF",
            "error": str(e)
        }

        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0'   )
