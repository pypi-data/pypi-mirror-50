##rvTTS
rvTTS is a cli tool for converting text to mp3 files using ResponsiveVoice's API.

------------


### Features
- Automatically tokenizing sentences. Special thanks to pndurette (https://github.com/pndurette/gTTS) for his tokenizer.
- Support unlimited text length.
- Adjustable pitch, rate, volume.

------------


### Installation
`pip install rvtts`

------------

### Usage
`rvtts [OPTIONS]`

**Options**
* Read from stdin:
`-t, --text  <text>`

* Read from file:
`-i, --input <filename>`

* Output file:
`-o, --output <filename>`

* Adjust pitch. Valid range *0-1*. Default: **0.5**:
`--pitch <range>`

* Adjust rate. Valid range *0-1*. Default: **0.5**:
`--rate <range>`

* Adjust volume. *0-1*. Default: **1**:
`--vol <range>`

* Output voice. Default: **english_us_male**:
`-v, --voice <voicename>`

* Debug mode:
`-d, --debug`

* Print all supported voices and exit:
`-l, --lang`

* Show the version and exit:
`--version`

### Examples
* Convert from stdin to `hello.mp3`:
`rvtts --text "hello wold" -o hello.mp3`

* Convert Vietnamese text:
`rvtts --text "một hai ba bốn năm sáu" -o test.mp3 -v vietnamese_female`

* Convert from `chuong-0001.txt` to `chuong-0001.mp3`:
`rvtts -i chuong-0001.txt -o chuong-0001.txt -v vietnamese_male`

* Print all supported voices:
`rvtts --lang`



