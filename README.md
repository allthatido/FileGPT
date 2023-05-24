<h1 align="center"> FileGPT: Local cognitive search over a pdf </h1>
</br>
<p align="center"><img src="media/FileGPT.png"></p>
</br>
</br>

## Steps to run the model locally
</br>
 
 - clone this repository
   ```bash
      git clone https://github.com/allthatido/FileGPT.git

 - Navigate to the `models` folder

 - Download the LLama family model (GGML V3 only) you want to test. Refer to README.md in the `models` folder.

 - install dependencies. If you get an error for the below command, install each library indivisually using pip install. Windows users may have to install latest Visual C++ libraries from [here](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
   ```bash
      pip install -r requirements.txt

 - Start streamlit app
   ```bash
      streamlit run app.py
 
 - Open browser and go to http://localhost:8501/
