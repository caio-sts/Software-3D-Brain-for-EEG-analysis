"""""
import time
import requests
import requests_cache

from flask import Flask, render_template, request, jsonify


from pyedflib import highlevel


signals, signal_headers, header = highlevel.read_edf('OA 04-04-2022_NFBK System.edf')
for i in range(len(signal_headers)):
    print()  # prints 256

print(header)


app = Flask(__name__)

requests_cache.install_cache('github_cache', backend='sqlite', expire_after=180)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # user inputs
        first = request.form.get('first')
        second = request.form.get('second')
        # api call
        url = "https://api.github.com/search/users?q=location:{0}+language:{1}".format(first, second)
        now = time.ctime(int(time.time()))
        response = requests.get(url)
        print("Time: {0} / Used Cache: {1}".format(now, response.from_cache))
        # return json
        return jsonify(response.json())
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
"""""

import os
import shutil

import numpy as np
import mne
import matplotlib

sample_path = mne.datasets.sample.data_path()
subjects_dir = os.path.join(sample_path, 'subjects')
eegFile = mne.io.read_raw_edf('OA 04-04-2022_NFBK System.edf', preload=True)


data, times = eegFile[:, :20]
print(data.shape)
start, stop = eegFile.time_as_index([100, 115])  # 100 s to 115 s data segment
data, times = eegFile[:306, start:stop]
print(data.shape)
print(times.shape)
print(times.min(), times.max())

picks = mne.pick_types(eegFile.info, meg='mag', exclude=[])
print(picks)


"""""
eegFile.rename_channels(lambda s: s.strip("."))
eegFile.set_montage("standard_1020", match_case=False)
eegFile.set_eeg_reference("average")

eegFile.plot(n_channels=64, duration=5, scalings={"eeg": 75e-6}, start=10)


print(eegFile.info)
print(eegFile.ch_names[:2])
data, times = eegFile[:3, :10]
print(data.shape)
print(times)
print(data)

#eegFile.crop(tmax=60)

#start, stop = eegFile.time_as_index([0, 10])  # 100 s to 115 s data segment
data, times = eegFile[:, :]

picks = mne.pick_types(eegFile.info, meg='mag', exclude=[])
#print(picks)
#data, times = eegFile[picks[:10], start:stop]

import matplotlib.pyplot as plt
import plotly.plotly as py

plt.plot(times, data.T)
plt.xlabel('time (s)')
plt.ylabel('EEG data (T)')

update = dict(layout=dict(showlegend=True), data=[dict(name=raw.info['ch_names'][p]) for p in picks[:10]])
py.iplot_mpl(plt.gcf(), update=update)

# Show the condition names, and reassure ourselves that baseline correction has
# been applied.
for e in evokeds_list:
    print(f'Condition: {e.comment}, baseline: {e.baseline}')


conds = ('aud/left', 'aud/right', 'vis/left', 'vis/right')
evks = dict(zip(conds, evokeds_list))

evks['aud/left'].plot(exclude=[])

evks['aud/left'].plot(picks='mag', spatial_colors=True, gfp=True)

times = np.linspace(0.05, 0.13, 5)
evks['aud/left'].plot_topomap(ch_type='mag', times=times, colorbar=True)

fig = evks['aud/left'].plot_topomap(ch_type='mag', times=0.09, average=0.1)
fig.text(0.5, 0.05, 'average from 40-140 ms', ha='center')
"""""