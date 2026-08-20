# task 2

n8n flow: csv comes in on a webhook, we check email/phone against people we already have, ping an alert if it is a duplicate.

`known_identities.csv` is dumped from `../task1/data/people.db`. n8n has no sqlite node so this file is the link.

## setup

```
python export_identities.py
```

n8n cloud (or local): import `duplicate_person_alert.json`, change the alert url on **send alert** (webhook.site is ok), activate, copy the webhook url.

```
curl -F "data=@sample_incoming.csv" https://YOUR-HOST/webhook/new-people-csv
```

Tanvi + Ritu should alert. Someone New should not.

If fetch known people 404s, the csv is not on github yet — put the file on a public url and paste it in that node.

## stuck

Root cause of execution 6: the csv webhook had a binary property name configured, but binary data capture was off. n8n discarded the upload entirely, so parse upload failed with "item has no binary field 'data'".

What changed: enabled binaryData on the csv webhook, pointed parse upload at data0 for multipart uploads, and made both parse nodes explicit csv operations.

Wanted to query sqlite from n8n directly. no built-in node, and a python webhook would be counted as code. exported emails/phones to csv and let n8n compareDatasets do the check.

compareDatasets only joins one field at a time so emails and phones are two branches merged. a bit annoying but it flags both.
