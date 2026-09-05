import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from src.model import create_signature_model

def train_model(dataset_dir='dataset', epochs=25, batch_size=32):
    img_size = (128, 128)
    
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=5,
        zoom_range=0.1,
        width_shift_range=0.05,
        height_shift_range=0.05
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_data = train_datagen.flow_from_directory(
        os.path.join(dataset_dir, 'train'),
        target_size=img_size,
        batch_size=batch_size,
        class_mode='binary',
        color_mode='grayscale'
    )
    
    val_data = val_datagen.flow_from_directory(
        os.path.join(dataset_dir, 'val'),
        target_size=img_size,
        batch_size=batch_size,
        class_mode='binary',
        color_mode='grayscale'
    )
    
    model = create_signature_model(input_shape=(128, 128, 1))
    model.summary()
    
    checkpoint = ModelCheckpoint(
        'models/signature_cnn_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max'
    )
    
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    
    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=epochs,
        callbacks=[checkpoint, early_stop]
    )
    
    print("✅ Training completed! Model saved to models/signature_cnn_model.h5")
    return model, history
