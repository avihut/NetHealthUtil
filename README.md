_A solution to a home exercise_

# Network Health Utility

A utility for inspecting current communication status to network locations by checking their visible IP addresses, connection latency and the download speed from them.

The utility is meant to be operable from the command line:

```
nethealth --tests-file FILE [--results-file FILE]
```

The utility expects a tests JSON file containing a network health tests configuration. This is the only way to indicate to the utility what tests will actually run. A human-readable description of the progress of the utility will be printed to the standard output.

Actual results will be saved to a results file in JSON format if a path is given. If the file already contains existing results, new results will be appended at the end. If comparable the difference between the new results and the previous will be written to the standard output.

Table of contents
=================

  * [Tests File Format](#tests-file-format)
  * [Results File Format](#results-file-format)
  * [Installing and Running the Utility](#installing-and-running-the-utility)

### Tests File Format

```JSON
[
  {
    "DNSLookup": {
      "URL": "accezz.io"
    }
  },
  {
    "DNSLookup": {
      "URL": "yahoo.com"
    }
  },
  {
    "Connectivity": {
      "URL": "http://download.thinkbroadband.com/5MB.zip"
    }
  }
]
```

The file is a JSON format. The top-level element is a list wherein each object is an operation. The operation has a single key which is its name. The key's data is another dictionary containing the parameters of the operation.

### Results File Format

```JSON
[
  {
    "DNSLookupResult": {
      "Time": "2017-01-24T16:51:25.795359",
      "URL": "accezz.io",
      "IPv4": [
        "50.63.202.27"
      ],
      "IPv6": []
    }
  },
  {
    "DNSLookupResult": {
      "Time": "2017-01-24T16:51:25.814077",
      "URL": "yahoo.com",
      "IPv4": [
        "98.138.253.109",
        "206.190.36.45",
        "98.139.183.24"
      ],
      "IPv6": [
        "2001:4998:c:a06::2:4008",
        "2001:4998:44:204::a7",
        "2001:4998:58:c02::a9"
      ]
    }
  },
  {
    "ConnectivityResult": {
      "SpeedTestResult": {
        "Time": "2017-01-24T16:51:30.171754",
        "URL": "http://download.thinkbroadband.com/5MB.zip",
        "AvgSpeedBps": 24027920.33994941
      },
      "PingResult": {
        "Time": "2017-01-24T16:51:28.235411",
        "URL": "http://download.thinkbroadband.com/5MB.zip",
        "PingTimes": [
          79.258,
          98.843,
          81.92
        ]
      }
    }
  }
]
```

## Installing and Running the Utility

_I'm still working on making the deployment and running of the utility easier. Something that has proved a bit more elusive since I chose to use Python 3.6. But in the meantime following these requirements will allow the utility to run._

To install the utility you will need Python version +3.2

1. Checkout this repository
2. Change the directory to `py`
3. Run the script `install_dependencies.sh`
4. Run the utility `py/src/nethealth`
