# app.py
from flask import Flask, request, jsonify, render_template
from PIL import Image
from io import BytesIO
import os
import random # For placeholder predictions

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Placeholder "AI" Functions (Updated for Weapon Prediction from Wound) ---

def predict_wound_cause(image_data):
    # (Same as before - placeholder for wound cause)
    causes = ["Sharp object injury", "Blunt force trauma", "Gunshot wound", "Burn", "Abrasion", "Laceration"]
    return random.choice(causes)

def estimate_time_of_death(image_data):
    # (Same as before - placeholder for time of death)
    return "Requires Medical Examination"

def predict_weapon_type(wound_diameter):
    # Placeholder weapon prediction based on WOUND DIAMETER (still simplified)
    if wound_diameter is None:
        return "Cannot predict weapon without wound diameter estimate"
    diameter = float(wound_diameter) # Ensure diameter is treated as number

    if diameter > 10: # Larger wound diameter
        return "Likely a larger weapon: e.g., Axe, Machete, Large caliber firearm"
    elif diameter > 5: # Medium wound diameter
        return "Possibly a medium weapon: e.g., Knife, Medium caliber firearm, Club"
    elif diameter > 1: # Smaller wound diameter
        return "Could be a smaller weapon: e.g., Small knife, Sharp object, Ice pick"
    else: # Very small or no diameter estimated
        return "Weapon type uncertain, wound may be superficial or image quality limited"

# --- Image Dimension Function (reused) ---
def get_image_dimensions(image_data):
    try:
        image = Image.open(BytesIO(image_data))
        width, height = image.size
        return width, height
    except Exception as e:
        return None, None, str(e)

# --- Placeholder Wound Diameter Calculation (very simplified - reused) ---
def estimate_wound_diameter(image_data):
    # (Same placeholder diameter calculation based on image width)
    width, height = get_image_dimensions(image_data)
    if width is not None:
        return round(width / 10, 2) # Just an example calculation - not real diameter
    return None


# --- Flask Routes ---

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze_wound', methods=['POST'])
def analyze_wound_image():
    if 'woundImage' not in request.files: # Changed to 'woundImage' to match frontend
        return jsonify({'error': 'No wound image provided'}), 400

    wound_image_file = request.files['woundImage'] # Changed to 'woundImage'
    if wound_image_file.filename == '':
        return jsonify({'error': 'No selected wound image'}), 400
    wound_image_data = wound_image_file.read()

    width, height = get_image_dimensions(wound_image_data)
    wound_diameter = estimate_wound_diameter(wound_image_data) # Placeholder diameter
    predicted_cause = predict_wound_cause(wound_image_data) # Placeholder cause prediction
    time_of_death_estimate = estimate_time_of_death(wound_image_data) # Placeholder time of death

    if width is None or height is None:
        return jsonify({'error': 'Error processing wound image', 'details': height}), 500

    filename = wound_image_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(wound_image_data)

    response_data = {
        'width': width,
        'height': height,
        'filename': filename,
        'wound_diameter': wound_diameter, # Include diameter in response
        'predicted_cause': predicted_cause, # Include predicted cause
        'time_of_death_estimate': time_of_death_estimate # Include time of death estimate
    }
    return jsonify(response_data)


@app.route('/analyze_weapon', methods=['POST'])
def analyze_weapon_image(): # Route name remains 'analyze_weapon' but now processes WOUND image to predict weapon
    if 'weaponImage' not in request.files: # Frontend still sends 'weaponImage' key
        return jsonify({'error': 'No wound image provided for weapon analysis'}), 400 # Updated error message

    wound_image_file = request.files['weaponImage'] # Frontend still sends 'weaponImage' key
    if wound_image_file.filename == '':
        return jsonify({'error': 'No selected wound image for weapon analysis'}), 400 # Updated error message
    wound_image_data = wound_image_file.read() # Now processing WOUND image for weapon analysis

    width, height = get_image_dimensions(wound_image_data)
    wound_diameter_for_weapon_prediction = estimate_wound_diameter(wound_image_data) # Estimate diameter from WOUND image
    predicted_weapon = predict_weapon_type(wound_diameter_for_weapon_prediction) # Predict weapon based on wound diameter

    if width is None or height is None:
        return jsonify({'error': 'Error processing wound image for weapon analysis', 'details': height}), 500 # Updated error message

    filename = wound_image_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(wound_image_data)

    response_data = {
        'width': width,
        'height': height,
        'filename': filename,
        'wound_diameter_estimate': wound_diameter_for_weapon_prediction, # Added wound diameter to weapon analysis report
        'predicted_weapon': predicted_weapon # Predict weapon based on wound diameter
    }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)