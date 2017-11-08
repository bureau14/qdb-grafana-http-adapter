# qdb-grafana-http-adapter

## Requirements

- windows OS (x86/amd64), linux, freebsd, ~~macOS~~
- qdb-api-python (https://github.com/bureau14/qdb-api-python) installed
- grafana server running
- SimpleJSON (for Grafana) plugin installed

## How to use it ?

### Create a dummy Timeserie with random points
`python main.py`

### Start the API

`pip install -r requirements.txt`
`python app.py`

## In Grafana

### Accessing grafana interface

Go to grafana web interface (default is `http://localhost:3000`)
Default credentials (`admin/admin`)

Then you should see an interface similar to the below
<img src="https://i.imgur.com/zBaATFW.png" width="700"/>

### Requirements

`SimpleJSON` is required to crunch the data from the API

Go to `plugins` section, then `Find more plugins on Grafana.com`, SimpleJSON should be in the list of plugins

### Adding a Data Source

Once `SimpleJSON` plugin is installed, go to `Data sources` section, then click on the `Add data source` link

Under config tab : 

- select a name for your data source
- select `SimpleJson` as a type
- use the URI of the API as a Data Source : `http://$(MY_HOST)`
- then click on Save & Test

<img src="https://i.imgur.com/vP5xbo1.png" width="500"/>

### Displaying the Data

- click on `Create a new Dashboard` under home view panel
- then, click on the pictogram `graph` or `table`
- click on Widget label to access configuration (e.g : 'Panel Title')
- then on `Edit button`
- You'll see a dropdown to select your data source, and another one to add one or more Timeserie target(s)


### Warning
If you use a special character such as `:`, `,`, `%` in your timeseries name nor columns name, you will need change the delimiter `settings.py`/`[SEPARATOR_TS_LABEL]`; it will be the pattern to keep out of columns/timeseries aliases.

To improve performances on grafana panel, we've set a variable in `settings.py`/`[ARBITRATY_NB_DATAPOINTS]`, which'll limit the number of datapoints in API Output.

#### Note for macOS users

`qdb-api-python` is not yet totally supported on macOS X
