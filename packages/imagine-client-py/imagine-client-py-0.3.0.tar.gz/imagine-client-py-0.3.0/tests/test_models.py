import os

import pytest

from imagine_client_py import ImagineClient, ImageBasedModel


@pytest.fixture
def imagine_client():
    return ImagineClient({
            'api_key': os.environ.get("IMAGINE_API_KEY"),
            'client_id': os.environ.get("IMAGINE_CLIENT_ID", "test")
        })

@pytest.fixture
def image_file():
    tests_dir = os.path.abspath(os.path.dirname(__file__))
    image_path = os.path.join(tests_dir, 'fixtures', 'test-face.jpg')
    return image_path

test_specs = [
    {
        'name': 'Phenomenal Face',
        'model_id': 'phenomenal-face',
        'result_type': 'face',
        'expected_response_keys': {'data', 'id', 'meta', 'type'},
        'expected_meta': {
            "age": "float",
            "gender": "string",
            "height": "float",
            "weight": "float"
        },
        'label_correction': {
            'height': 159.0,
            'weight': 65.0,
            'age': 36.0,
            'gender': 'male'
        },
        'label_prediction': {
            'height': 159.0,
            'weight': 65.0,
            'age': 36.0,
            'gender': 'male'
        }
    },
    {
        'name': 'Happy Face',
        'model_id': 'happy-face',
        'result_type': 'face',
        'expected_response_keys': {'data', 'id', 'meta', 'type'},
        'expected_meta': {
            'upset': 'float',
            'calm': 'float',
            'happy': 'float',
            'sad': 'float',
            'surprised': 'float',
            'unknown': 'float'
        },
        'label_correction': {
            'upset': 0.0,
            'calm': 0.7,
            'happy': 0.1,
            'sad': 0.1,
            'surprised': 0.0,
            'unknown': 0.1
        },
        'label_prediction': {
            'upset': 0.0,
            'calm': 1.0,
            'happy': 0.0,
            'sad': 0.0,
            'surprised': 0.0,
            'unknown': 0.0
        }
    },
    {
        'name': 'Face Detector',
        'model_id': 'face-detector',
        'result_type': 'face',
        'expected_response_keys': {'data', 'id', 'meta', 'type'},
        'expected_meta': {
            'face': 'float',
            'no_face': 'float'
        },
        'label_correction': {
            'face': 1.0,
            'no_face': 0.0
        },
        'label_prediction': {
            'face': 0.95,
            'no_face': 0.05
       }
    },
    {
        'name': 'Food Detector',
        'model_id': 'food-detector',
        'result_type': 'food',
        'expected_response_keys': {'data', 'id', 'meta', 'type'},
        'expected_meta': {
            'food': 'float',
            'not_food': 'float'
        },
        'label_correction': {
            'food': 0.0,
            'not_food': 1.0
        },
        'label_prediction': {
            'food': 0.05,
            'not_food': 0.95
       }
    },
    {
        'name': 'Manna',
        'model_id': 'manna',
        'result_type': 'food',
        'expected_response_keys': {'data', 'id', 'meta', 'type'},
        'expected_meta': {
            'healthy': 'float',
            'unhealthy': 'float'
        },
        'label_correction': {
            'healthy': 0.0,
            'unhealthy': 1.0
        },
        'label_prediction': {
            'healthy': 0.05,
            'unhealthy': 0.95
       }
    }
]

def test_all_models(imagine_client, image_file):
    for spec in test_specs:
        model = ImageBasedModel.create(imagine_client, spec['model_id'])
        with open(image_file, 'rb') as ifp:
            # Perform the model's inference, on the image.
            result = model.infer(ifp)

        assert set(result.keys()) == spec['expected_response_keys'], '{} error on /infer'.format(spec['name'])
        assert result['type'] == spec['result_type'], '{} error on /infer'.format(spec['name'])
        assert result['meta'] == spec['expected_meta'], '{} error on /infer'.format(spec['name'])
        assert result['data'].keys() == spec['expected_meta'].keys(), '{} error on /infer'.format(spec['name'])

        image_id = result['id']
        labels = spec.get('label_correction')
        if labels is not None:
            labels['id'] = image_id
            model.insert_correction(labels, {})

        labels = spec.get('label_prediction')
        if labels is not None:
            labels['id'] = image_id
            model.insert_correction(labels, {})
