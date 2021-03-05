# Credit Risk Model with Driverless AI - Wave App
This application uses H2O Driverless AI to predict if a customer will default.

## Running this App Locally

### System Requirements 
1. Python 3.6+
2. pip3

### 1. Run the Wave Server
New to H2O Wave? We recommend starting in the documentation to [download and run](https://h2oai.github.io/wave/docs/installation) the Wave Server on your local machine. Once the server is up and running you can easily use any Wave app. 

### 2. Setup Your Python Environment

```bash
$ git clone https://github.com/a-ghorbani/h2o-wave-apps.git
$ cd wave-app-credit-risk
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

### 3. Run the App

```bash
wave run app
```

Note! If you did not activate your virtual environment this will be:
```bash
./venv/bin/wave run app
```

### 4. View the App
Point your favorite web browser to [localhost:10101](http://localhost:10101)
