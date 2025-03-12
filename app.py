from flask import Flask, render_template, request # type: ignore
import tensorflow as tf # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from keras.models import load_model # type: ignore
from keras.preprocessing import image # type: ignore
from keras.metrics import AUC # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore

app = Flask(__name__)

dependencies = {
    'auc_roc': AUC
}

# Load model
model = load_model('plant.h5')

# Load CSV data
csv_data = pd.read_csv(r'/Users/rehanrasool/Desktop/Project/Medicinal System/medicinal.csv')

# Define verbose_name mapping (if not already loaded from CSV)
verbose_name = {
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


def predict_label(img_path):
    test_image = image.load_img(img_path, target_size=(180, 180))
    test_image = image.img_to_array(test_image) / 255.0
    test_image = test_image.reshape(1, 180, 180, 3)

    predict_x = model.predict(test_image)
    classes_x = np.argmax(predict_x, axis=1)

    predicted_name = verbose_name[classes_x[0]]
    
    # Fetch all fields from CSV based on Scientificname
    row = csv_data[csv_data['Scientificname'] == predicted_name]
    if not row.empty:
        result = {
            'Scientificname': row.iloc[0]['Scientificname'],
            'Biologicalname': row.iloc[0]['Biologicalname'],
            'Medicinalvalue': row.iloc[0]['Medicinalvalue'],
            'Family': row.iloc[0]['Family'],
            'CommonUses': row.iloc[0]['CommonUses'],
            'ActiveCompounds': row.iloc[0]['ActiveCompounds'],
            'ToxicityLevel': row.iloc[0]['ToxicityLevel'],
            'GeographicalDistribution': row.iloc[0]['GeographicalDistribution'],
            'GrowthHabit': row.iloc[0]['GrowthHabit'],
            'PartsUsed': row.iloc[0]['PartsUsed'],
            'PreparationMethods': row.iloc[0]['PreparationMethods'],
            'ConservationStatus': row.iloc[0]['ConservationStatus']
        }
    else:
        result = {field: "Not found" for field in csv_data.columns}
    
    return result, img_path

@app.route("/")
@app.route("/first")
def first():
    return render_template('first.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']

        img_path = "static/tests/" + img.filename
        img.save(img_path)

        result, img_path = predict_label(img_path)

        return render_template("prediction.html", result=result, img_path=img_path)

@app.route("/performance")
def performance():
    return render_template('performance.html')

@app.route("/chart")
def chart():
    return render_template('chart.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)