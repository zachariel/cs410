import requests

from classifier.onet_model import load_data

data_train, data_set = load_data()
api_url = 'http://localhost:8000/classification/jobs/classify/'

for i in range(10):
    content = data_set.data[i]
    filename = data_set.filenames[i][-47:-4]
    payload = { 'content': content, 'reference_number': filename }

    r = requests.post(api_url, data=payload, auth=('zachariel', 'z4ch4r13l'))
    print(r.text)

