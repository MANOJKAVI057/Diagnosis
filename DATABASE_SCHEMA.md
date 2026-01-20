# Database Schema

## MongoDB Collections

### Users Collection
```javascript
{
  _id: ObjectId,
  username: String (unique, required, min 3 chars),
  password: String (hashed with bcrypt),
  name: String (required),
  age: Number (required),
  gender: String (Male/Female/Other/Prefer not to say),
  contact: String (required),
  school_college: String (required, max 10 chars),
  gmail: String (required, unique),
  medical_history: String (optional),
  emergency_contact: String (optional),
  theme: String (light/dark, default: light),
  language: String (en/ta, default: en),
  created_at: DateTime,
  updated_at: DateTime
}
```

### Diagnoses Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (reference to users._id),
  vitals: {
    temperature: String (in Fahrenheit),
    heart_rate: String (bpm),
    systolic_bp: String (mmHg),
    diastolic_bp: String (mmHg),
    respiratory_rate: String (/min),
    oxygen_saturation: String (%)
  },
  algorithm: String (logistic_regression/svm/cnn/lstm),
  result: {
    condition: String,
    severity: String (normal/moderate/critical),
    confidence: Number (0.0-1.0),
    algorithm: String
  },
  image_path: String (optional, path to uploaded image),
  created_at: DateTime
}
```

## Indexes

### Users Collection
- `username`: Unique index
- `gmail`: Unique index
- `school_college`: Index for password recovery

### Diagnoses Collection
- `user_id`: Index for faster queries
- `created_at`: Index for sorting and filtering
- `user_id + created_at`: Compound index for user history queries

## Relationships

- One User can have many Diagnoses (One-to-Many)
- Each Diagnosis belongs to one User




