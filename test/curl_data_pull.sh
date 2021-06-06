#!/bin/sh

# Change the Authorization: Bearer <access_token> if script failing using the curl_token_gen.sh
curl -X POST \
  https://services.sentinel-hub.com/api/v1/process \
  -o data.txt \
  -H 'Authorization: Bearer eyJraWQiOiJzaCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwZTk3OGNkNi1iNTFjLTQ1OGEtODVmZS1kZGE4NWQ3ODQ4NzMiLCJhdWQiOiJmMmRjOTJkNC1iYjAxLTRjMGMtYTcyNy02MzI0MjkzYWZmNmUiLCJqdGkiOiJjNGY5MGQ1ZC00NTBjLTRjOGMtOGM4Zi1lNzQ1ZmVhZTYwNTUiLCJleHAiOjE2MjI5MTYyMDUsIm5hbWUiOiJNaXRjaGVsbCBSZWFkIiwiZW1haWwiOiJtaXRjaGVsbC5nLnJlYWRAZ21haWwuY29tIiwiZ2l2ZW5fbmFtZSI6Ik1pdGNoZWxsIiwiZmFtaWx5X25hbWUiOiJSZWFkIiwic2lkIjoiMWY3MWFhZDgtNzhiMy00MmEzLTk2M2QtMmEwNTI0MjFkNzYyIiwiZGlkIjoxLCJhaWQiOiI1ZjRhOWE4Ni05OGVkLTQ3NzktOGYzMi1kNGY4OWZkMDliYTIiLCJkIjp7IjEiOnsicmEiOnsicmFnIjoxfSwidCI6MTEwMDB9fX0.KYXKcV7xz-_6iHhIEKaLk0NgmJAdMq6TOcvjjq0G74QjEPTf3eHdKD8bHAcrVKBIkx8V_TN4gNKNKDRCxVVTf6OOnNdbHgo8Z8kpSIgJPn08asbL_P_IJdLLZN7PijszqkjvlQtvk1vuH512qmUqDVP9_PV07Si2zuQI8fMlKx1Yx5ISmPo5HVVjscFD_LDwYP5m8zLCHD8wehg18KyPmDQ1qIYU7K9s2zooNqK3mhWAZpOuxos8WR27gE6dekJnwmse4eCSPxfRr9LxzybI-bXfEgVNhqiJnSCLfRsfWA9occMmAJiPOKksavvQwO8nA3ssbeO8-S3_7nDRmu7nGg' \
  -F 'request={
    "input": {
        "bounds": {
            "properties": {
                "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            },
            "bbox": [
                13.822174072265625,
                45.85080395917834,
                14.55963134765625,
                46.29191774991382
            ]
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": "2018-10-01T00:00:00Z",
                        "to": "2018-12-31T00:00:00Z"
                    }
                }
            }
        ]
    },
    "output": {
        "width": 512,
        "height": 512
    }
}' \
  -F 'evalscript=//VERSION=3

function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: {
      bands: 3,
      sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
    }
  }
}

function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
}'