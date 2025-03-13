 
# HerbEsentia - Medicinal Plant Identification System
#  @Darrehan
 the website might not produce output its deployed on render it need adavance image processing power it will work  fine on your pc 

![HerbEsentia Logo](static/images/favicon.ico)

**HerbEsentia** is an open-source initiative dedicated to revolutionizing the identification, classification, and analysis of medicinal plants. This project provides a comprehensive dataset encompassing **202 distinct classes** of medicinal plants, enabling advanced research in **phytochemistry, pharmacognosy, and machine learning-driven botanical studies**. HerbEsentia is designed to serve as a collaborative platform for researchers, data scientists, and medical professionals to enhance medicinal plant analysis, particularly in **India and Kashmir**.



## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [File Structure](#file-structure)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Contributing](#contributing)
   - [Branching Strategy](#branching-strategy)
   - [Pull Request Process](#pull-request-process)
7. [Dataset](#dataset)
8. [Model Training](#model-training)
9. [License](#license)
10. [Acknowledgments](#acknowledgments)


## Project Overview

HerbEsentia is an open-source project that leverages **deep learning** and **computer vision** to identify and classify medicinal plants. The system uses a pre-trained model (`plant.h5`) to predict the biological name of a plant based on an uploaded image. It then compares the prediction with a comprehensive dataset (`medicinal.csv`) to provide detailed information about the plant, including its medicinal value, family, common uses, and more.



## Features

- **Medicinal Plant Identification**: Upload an image of a plant, and the system will predict its biological name.
- **Comprehensive Dataset**: Detailed information about 202 medicinal plants, including medicinal value, toxicity level, and geographical distribution.
- **User-Friendly Interface**: Simple and intuitive web interface for uploading images and viewing results.
- **Open-Source**: Fully open-source, allowing researchers and developers to contribute and improve the system.


## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/HerbEsentia.git
   cd HerbEsentia

   pip install -r requirements.txt

   python app.py

#   HerbEsentia CNN (VGG16 and Xception Architecture)



