from flask import Flask, render_template, request, redirect, url_for # type: ignore
api/app.py # type: ignore
import tensorflow as tf # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from keras.preprocessing import image # type: ignoreß
from keras.metrics import AUC # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore
import os
import requests # type: ignore
import uuid

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load ML Model
def load_ml_model():
    try:
        # Download model if not exists
        MODEL_URL = "https://github.com/darrehanrasool/Herbalist/releases/download/v1.0.0/plant.h5"
        MODEL_PATH = "plant.h5"
        
        if not os.path.exists(MODEL_PATH):
            print("Downloading model...")
            response = requests.get(MODEL_URL, stream=True)
            if response.status_code == 200:
                with open(MODEL_PATH, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Model downloaded successfully.")
        
        # Load model
        dependencies = {'auc_roc': AUC}
        model = load_model(MODEL_PATH, custom_objects=dependencies)
        print("✅ Model loaded successfully")
        return model
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return None

# Load Dataset
def load_dataset():
    try:
        CSV_URL = "https://github.com/darrehanrasool/Herbalist/releases/download/v1.0.1/medicinal.csv"
        CSV_PATH = "medicinal.csv"
        
        if not os.path.exists(CSV_PATH):
            print("Downloading dataset...")
            response = requests.get(CSV_URL)
            if response.status_code == 200:
                with open(CSV_PATH, 'wb') as f:
                    f.write(response.content)
                print("Dataset downloaded successfully.")
        
        # Load CSV
        df = pd.read_csv(CSV_PATH)
        print(f"✅ Dataset loaded: {len(df)} plants")
        return df
    except Exception as e:
        print(f"❌ Dataset loading failed: {e}")
        return None

# Initialize
model = load_ml_model()
dataset = load_dataset()

# Plant class mapping
PLANT_CLASSES = {
0: 'Abelmoschus sagittifolius',
1: 'Abrus precatorius',
2: 'Abutilon indicum',
3: 'Acanthus integrifolius',
4: 'Acorus tatarinowii',
5: 'Agave americana',
6: 'Ageratum conyzoides',
7: 'Allium ramosum',
8: 'Alocasia macrorrhizos',
9: 'Aloe vera',
10: 'Alpinia officinarum',
11: 'Amomum longiligulare',
12: 'Ampelopsis cantoniensis',
13: 'Andrographis paniculata',
14: 'Angelica dahurica',
15: 'Ardisia sylvestris',
16: 'Artemisia vulgaris',
17: 'Artocarpus altilis',
18: 'Artocarpus heterophyllus',
19: 'Artocarpus lakoocha',
20: 'Asparagus cochinchinensis',
21: 'Asparagus officinalis',
22: 'Averrhoa carambola',
23: 'Baccaurea sp',
24: 'Barleria lupulina',
25: 'Bengal Arum',
26: 'Berchemia lineata',
27: 'Bidens pilosa',
28: 'Bischofia trifoliata',
29: 'Blackberry Lily',
30: 'Blumea balsamifera',
31: 'Boehmeria nivea',
32: 'Breynia vitis',
33: 'Caesalpinia sappan',
34: 'Callerya speciosa',
35: 'Callisia fragrans',
36: 'Calophyllum inophyllum',
37: 'Calotropis gigantea',
38: 'Camellia chrysantha',
39: 'Caprifoliaceae',
40: 'Capsicum annuum',
41: 'Carica papaya',
42: 'Catharanthus roseus',
43: 'Celastrus hindsii',
44: 'Celosia argentea',
45: 'Centella asiatica',
46: 'Citrus aurantifolia',
47: 'Citrus hystrix',
48: 'Clausena indica',
49: 'Cleistocalyx operculatus',
50: 'Clerodendrum inerme',
51: 'Clinacanthus nutans',
52: 'Clycyrrhiza uralensis fish',
53: 'Coix lacryma-jobi',
54: 'Cordyline fruticosa',
55: 'Costus speciosus',
56: 'Crescentia cujete Lin',
57: 'Crinum asiaticum',
58: 'Crinum latifolium',
59: 'Croton oblongifolius',
60: 'Croton tonkinensis',
61: 'Curculigo gracilis',
62: 'Curculigo orchioides',
63: 'Cymbopogon',
64: 'Datura metel',
65: 'Derris elliptica',
66: 'Dianella ensifolia',
67: 'Dicliptera chinensis',
68: 'Dimocarpus longan',
69: 'Dioscorea persimilis',
70: 'Eichhoriaceae crassipes',
71: 'Eleutherine bulbosa',
72: 'Erythrina variegata',
73: 'Eupatorium fortunei',
74: 'Eupatorium triplinerve',
75: 'Euphorbia hirta',
76: 'Euphorbia pulcherrima',
77: 'Euphorbia tirucalli',
78: 'Euphorbia tithymaloides',
79: 'Eurycoma longifolia',
80: 'Excoecaria cochinchinensis',
81: 'Excoecaria sp',
82: 'Fallopia multiflora',
83: 'Ficus auriculata',
84: 'Ficus racemosa',
85: 'Fructus lycii',
86: 'Glochidion eriocarpum',
87: 'Glycosmis pentaphylla',
88: 'Gonocaryum lobbianum',
89: 'Gymnema sylvestre',
90: 'Gynura divaricata',
91: 'Hemerocallis fulva',
92: 'Hemigraphis glaucescens',
93: 'Hibiscus mutabilis',
94: 'Hibiscus rosa sinensis',
95: 'Hibiscus sabdariffa',
96: 'Holarrhena pubescens',
97: 'Homalomena occulta',
98: 'Houttuynia cordata',
99: 'Imperata cylindrica',
100: 'Iris domestica',
101: 'Ixora coccinea',
102: 'Jasminum sambac',
103: 'Jatropha gossypiifolia',
104: 'Jatropha multifida',
105: 'Jatropha podagrica',
106: 'Justicia gendarussa',
107: 'Kalanchoe pinnata',
108: 'Lactuca indica',
109: 'Lantana camara',
110: 'Lawsonia inermis',
111: 'Leea rubra',
112: 'Litsea Glutinosa',
113: 'Lonicera dasystyla',
114: 'Lpomoea sp',
115: 'Maesa',
116: 'Mallotus barbatus',
117: 'Mangifera',
118: 'Melastoma malabathricum',
119: 'Mentha Spicata',
120: 'Microcos tomentosa',
121: 'Micromelum falcatum',
122: 'Millettia pulchra',
123: 'Mimosa pudica',
124: 'Morinda citrifolia',
125: 'Moringa oleifera',
126: 'Morus alba',
127: 'Mussaenda philippica',
128: 'Nelumbo nucifera',
129: 'Ocimum basilicum',
130: 'Ocimum gratissimum',
131: 'Ocimum sanctum',
132: 'Oenanthe javanica',
133: 'Ophiopogon japonicus',
134: 'Paederia lanuginosa',
135: 'Pandanus amaryllifolius',
136: 'Pandanus sp',
137: 'Pandanus tectorius',
138: 'Parameria Laevigata',
139: 'Passiflora foetida',
140: 'Pereskia Sacharosa',
141: 'Persicaria odorata',
142: 'Phlogacanthus turgidus',
143: 'Phrynium placentarium',
144: 'Phyllanthus Reticulatus Poir',
145: 'Piper betle',
146: 'Piper sarmentosum',
147: 'Plantago',
148: 'Platycladus orientalis',
149: 'Plectranthus amboinicus',
150: 'Pluchea pteropoda Hemsl',
151: 'Plukenetia volubilis',
152: 'Plumbago indica',
153: 'Plumeris rubra',
154: 'Polyginum cuspidatum',
155: 'Polyscias fruticosa',
156: 'Polyscias guilfoylei',
157: 'Polyscias scutellaria',
158: 'Polyscias zeylanica',
159: 'Premna serratifolia',
160: 'Pseuderanthemum latifolium',
161: 'Psidium guajava',
162: 'Psychotria reevesii Wall',
163: 'Psychotria rubra',
164: 'Quisqualis indica',
165: 'Rauvolfia',
166: 'Rauvolfia tetraphylla',
167: 'Rhinacanthus nasutus',
168: 'Rhodomyrtus tomentosa',
169: 'Ruellia tuberosa',
170: 'Sanseviera canaliculata Carr',
171: 'Sansevieria hyacinthoides',
172: 'Sarcandra glabra',
173: 'Sauropus androgynus',
174: 'Schefflera heptaphylla',
175: 'Schefflera venulosa',
176: 'Senna alata',
177: 'Sida acuta Burm',
178: 'Solanum Mammosum',
179: 'Solanum torvum',
180: 'Spilanthes acmella',
181: 'Spondias dulcis',
182: 'Stachytarpheta jamaicensis',
183: 'Stephania dielsiana',
184: 'Stereospermum chelonoides',
185: 'Streptocaulon juventas',
186: 'Syzygium nervosum',
187: 'Tabernaemontana divaricata',
188: 'Tacca subflabellata',
189: 'Tamarindus indica',
190: 'Terminalia catappa',
191: 'Tradescantia discolor',
192: 'Trichanthera gigantea',
193: 'Vernonia amygdalina',
194: 'Vitex negundo',
195: 'Xanthium strumarium',
196: 'Zanthoxylum avicennae',
197: 'Zingiber officinale',
198: 'Ziziphus mauritiana',
199: 'helicteres hirsuta',
   
}


# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def predict_plant(image_path):
    """Predict plant from image and return all data"""
    if model is None or dataset is None:
        # Return demo data if model not loaded
        return {
            'success': False,
            'error': 'Model not loaded',
            'demo': True,
            'data': {
                'Scientificname': 'Aloe vera',
                'Biologicalname': 'Aloe',
                'Medicinalvalue': 'Used for skin healing and moisturizing',
                'Family': 'Asphodelaceae',
                'CommonUses': 'Skin healing, moisturizing',
                'ActiveCompounds': 'Aloin, polysaccharides',
                'ToxicityLevel': 'Low',
                'GeographicalDistribution': 'Global',
                'GrowthHabit': 'Succulent',
                'PartsUsed': 'Leaves',
                'PreparationMethods': 'Gel extraction',
                'ConservationStatus': 'Not Evaluated',
                'Confidence': '98.7%'
            }
        }
    
    try:
        # Load and preprocess image
        img = image.load_img(image_path, target_size=(180, 180))
        img_array = image.img_to_array(img) / 255.0
        img_array = img_array.reshape(1, 180, 180, 3)
        
        # Make prediction
        prediction = model.predict(img_array, verbose=0)
        class_idx = np.argmax(prediction)
        confidence = np.max(prediction) * 100
        
        # Get plant name
        plant_name = PLANT_CLASSES.get(class_idx, 'Unknown')
        
        # Find plant in dataset
        plant_data = dataset[dataset['Scientificname'] == plant_name]
        
        if not plant_data.empty:
            result = {
                'success': True,
                'demo': False,
                'confidence': f"{confidence:.1f}%",
                'data': {
                    'Scientificname': plant_data.iloc[0]['Scientificname'],
                    'Biologicalname': plant_data.iloc[0]['Biologicalname'],
                    'Medicinalvalue': plant_data.iloc[0]['Medicinalvalue'],
                    'Family': plant_data.iloc[0]['Family'],
                    'CommonUses': plant_data.iloc[0]['CommonUses'],
                    'ActiveCompounds': plant_data.iloc[0]['ActiveCompounds'],
                    'ToxicityLevel': plant_data.iloc[0]['ToxicityLevel'],
                    'GeographicalDistribution': plant_data.iloc[0]['GeographicalDistribution'],
                    'GrowthHabit': plant_data.iloc[0]['GrowthHabit'],
                    'PartsUsed': plant_data.iloc[0]['PartsUsed'],
                    'PreparationMethods': plant_data.iloc[0]['PreparationMethods'],
                    'ConservationStatus': plant_data.iloc[0]['ConservationStatus']
                }
            }
        else:
            result = {
                'success': False,
                'error': 'Plant not found in database',
                'demo': False
            }
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'demo': False
        }

# ========== CLEAN ROUTES ==========

@app.route('/')
def home():
    """Homepage with all sections"""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """Upload page"""
    return render_template('upload.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded image"""
    if 'plant_image' not in request.files:
        return redirect(url_for('upload_page'))
    
    file = request.files['plant_image']
    
    if file.filename == '':
        return redirect(url_for('upload_page'))
    
    if not allowed_file(file.filename):
        return render_template('upload.html', error='Invalid file type. Please upload an image.')
    
    # Generate unique filename
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Predict plant
    result = predict_plant(filepath)
    
    # Add image path to result
    result['image_path'] = f"uploads/{filename}"
    
    # Render results page
    return render_template('results.html', result=result)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    if 'image' not in request.files:
        return {'error': 'No image provided'}, 400
    
    file = request.files['image']
    
    if not allowed_file(file.filename):
        return {'error': 'Invalid file type'}, 400
    
    # Save file
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Predict
    result = predict_plant(filepath)
    result['image_url'] = url_for('static', filename=f'uploads/{filename}', _external=True)
    
    return result

# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('index.html'), 500

# ========== RUN APP ==========

if __name__ == '__main__':
    print("\n" + "="*50)
    print("HERBALIST AI - Starting Server")
    print("="*50)
    print(f"Model: {'✅ Loaded' if model else '❌ Failed'}")
    print(f"Dataset: {'✅ Loaded' if dataset is not None else '❌ Failed'}")
    print(f"Plants: {len(PLANT_CLASSES)} classes")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("="*50)
    print("Server running on: http://localhost:5001")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)