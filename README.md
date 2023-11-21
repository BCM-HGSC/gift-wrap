# gift-wrap

A collection of wrappers used by the Submissions Team.

## Install

Barebones:
`pip install git+https://github.com/BCM-HGSC/gift-wrap.git`

## Usage

For Sample Tracker/Exemplar/CVL

```
from gift_wrap.hgsc.sample_tracker import Sample Tracker

sample_tracker = SampleTracker(token=YOUR_TOKEN, base_url=API_URL)

sample_tracker.post(sample_name="test", project="test", state_key="test", biobank_id= "test", some_other_key="another test")
```

The token is generated by the user using cognito (in the case of Sample Tracker and Exemplar)