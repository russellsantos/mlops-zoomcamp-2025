import model


class MockModel:
    def __init__(self, prediction_value):
        self.prediction_value = prediction_value
    
    def predict(self, features):
        return [self.prediction_value]


def test_base64_decode():
    base64_input="ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ=="    
    actual_result = model.base64_decode(base64_input)
    expected_result = {
        'ride': {
            'PULocationID': 130,
            'DOLocationID': 205,
            'trip_distance': 3.66
        },
        'ride_id': 256
    }
    assert actual_result == expected_result

def test_prepare_features():
    model_service = model.ModelService(model=None, model_version="Test123")
    ride = {
        'PULocationID': 130,
        'DOLocationID': 205,
        'trip_distance': 3.66
    }
    expected_features = {
        'PU_DO': '130_205',
        'trip_distance': 3.66
    }
    features = model_service.prepare_features(ride)
    assert features == expected_features

def test_predict():
    # Test with a mock model that returns a specific prediction
    mock_model = MockModel(10.0)
    model_service = model.ModelService(model=mock_model, model_version="Test123") 
    
    features = {
        'PU_DO': '130_205',
        'trip_distance': 3.66
    }
    
    prediction = model_service.predict(features)
    
    # Should return the mock prediction as a float
    expected_prediction = 10.0  
    assert prediction == expected_prediction


def test_lambda_handler():
    model_version = "Test123"
    mock_model = MockModel(10.0)
    model_service = model.ModelService(model=mock_model, model_version=model_version)
    event = {
        "Records": [{
            "kinesis": {
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ==",
            },
        }]
    }

    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        'predictions': [{
            'model': 'ride_duration_prediction_model',
            'version': model_version,
            'prediction': {
                'ride_duration': 10.0,
                'ride_id': 256
            }
        }]
    }
   