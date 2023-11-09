import json

from keras.src.preprocessing.image import ImageDataGenerator

# Ścieżka do katalogu treningowego
train_path = 'C:/Users/micha/OneDrive/Pulpit/AI/dog-breed-identification/Posegregowane/train'

# Tworzenie instancji ImageDataGenerator z odpowiednimi transformacjami dla danych treningowych
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

# Wykorzystanie ImageDataGenerator do stworzenia training_set
training_set = train_datagen.flow_from_directory(train_path,
                                                 target_size = (224, 224),
                                                 batch_size = 16,
                                                 class_mode = 'categorical')

# Pobierz słownik indeksów klas od generatora danych
class_indices = training_set.class_indices

# Odwróć słownik, aby indeksy były kluczami, a etykiety były wartościami
labels = {v: k for k, v in class_indices.items()}

# Zapisz słownik etykiet do pliku JSON
with open('Models/InceptionV3_own/class_indices.json', 'w') as json_file:
    json.dump(labels, json_file)



############################################################################################################
#Wykorzystanie słownika w modelu

# Załaduj słownik etykiet z pliku JSON
#with open('class_indices.json') as json_file:
#    labels = json.load(json_file)

# Teraz możesz użyć tego słownika do mapowania indeksów na etykiety
