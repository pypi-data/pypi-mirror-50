# -*- coding: utf-8 -*-
from rvtts.tokenizer import pre_processors, Tokenizer, tokenizer_cases
from rvtts.utils import _minimize, _len, _clean_tokens
from rvtts.version import __version__
import requests
import concurrent.futures
import logging
import click

class responsiveVoice:
    '''rvTTS
    
    A CLI tool to convert text to MP3 using ResponsiveVoice's API.
    
    Args:
        text (string): text to be converted.
        pitch (float, optional): adjust pitch output. Default is ``0.5``.
        rate (float, optional): adjust rate output. Default is ``0.5``.
        vol (float, optional): adjust volume output. Default is ``1``.
    '''
    API = 'https://code.responsivevoice.org/getvoice.php'
    CHARACTER_LIMIT = 100
    RV_HEADER = {'Referer':'https://responsivevoice.org/',
                    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3837.0 Safari/537.36 Edg/77.0.211.3'}
    PITCH = 0.5
    RATE = 0.5
    VOL = 1
    DEFAULT_VOICE = "english_us_male"
    VOICE = {}
    VOICE["vietnamese_female"] = {'tl':'vi','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["vietnamese_male"] = {'tl':'vi','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["english_us_male"] = {'tl':'en-US','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["english_us_female"] = {'tl':'en-US','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["english_uk_male"] = {'tl':'en-GB','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["english_uk_female"] = {'tl':'en-GB','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["arabic_male"] = {'tl':'ar','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["arabic_female"] = {'tl':'ar','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["english_australian_male"] = {'tl':'en-AU','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["english_australian_female"] = {'tl':'en-AU','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["chinese_male"] = {'tl':'zh-CN','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["chinese_female"] = {'tl':'zh-CN','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["hongkong_male"] = {'tl':'yue-HK','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["hongkong_female"] = {'tl':'yue-HK','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["taiwan_male"] = {'tl':'zh-TW','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["taiwan_female"] = {'tl':'zh-TW','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["czech_male"] = {'tl':'cs','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["czech_female"] = {'tl':'cs','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["danish_male"] = {'tl':'cs','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["danish_female"] = {'tl':'cs','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["deutsch_male"] = {'tl':'de','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["deutsch_female"] = {'tl':'de','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["dutch_male"] = {'tl':'nl','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["dutch_female"] = {'tl':'nl','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["filipino_female"] = {'tl':'fil-PH','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["finnish_male"] = {'tl':'fi','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["finnish_female"] = {'tl':'fi','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["french_male"] = {'tl':'fr','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["french_female"] = {'tl':'fr','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["french_canadian_male"] = {'tl':'fr-CA','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["french_canadian_female"] = {'tl':'fr-CA','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["creek_male"] = {'tl':'el','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["creek_female"] = {'tl':'el','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["hindi_male"] = {'tl':'hi','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["hindi_female"] = {'tl':'hi','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["hungarian_male"] = {'tl':'hu','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["hungarian_female"] = {'tl':'hu','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["indonesian_male"] = {'tl':'id','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["indonesian_female"] = {'tl':'id','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["italian_male"] = {'tl':'it','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["italian_female"] = {'tl':'it','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["japanese_male"] = {'tl':'jp','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["japanese_female"] = {'tl':'jp','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["korean_male"] = {'tl':'ko','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["korean_female"] = {'tl':'ko','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["latin_male"] = {'tl':'la','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["latin_female"] = {'tl':'la','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["norwegian_male"] = {'tl':'no','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["norwegian_female"] = {'tl':'no','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["polish_male"] = {'tl':'pl','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["polish_female"] = {'tl':'pl','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["portuguese_male"] = {'tl':'pt-PT','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["portuguese_female"] = {'tl':'pt-PT','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["romanian_female"] = {'tl':'ro','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["russian_male"] = {'tl':'ru','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["russian_female"] = {'tl':'ru','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["spanish_male"] = {'tl':'es','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["spanish_female"] = {'tl':'es','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["spanish_latin_american_male"] = {'tl':'es-419','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["spanish_latin_american_female"] = {'tl':'es-419','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["swedish_male"] = {'tl':'sv','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["swedish_female"] = {'tl':'sv','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["thai_male"] = {'tl':'th','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["thai_female"] = {'tl':'th','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}
    VOICE["turkish_male"] = {'tl':'tr','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'male'}
    VOICE["turkish_female"] = {'tl':'tr','pitch':PITCH,'rate':RATE,'vol':VOL,'gender':'female'}

    def __init__(self,text="",pitch=0.5,rate=0.5,vol=1,
            pre_processor_funcs=[
                pre_processors.tone_marks,
                pre_processors.end_of_line,
                pre_processors.abbreviations,
                pre_processors.word_sub
            ],
            tokenizer_func=Tokenizer([
                tokenizer_cases.tone_marks,
                tokenizer_cases.period_comma,
                tokenizer_cases.colon,
                tokenizer_cases.other_punctuation
            ]).run):
        self.text = text
        self.pitch = str(pitch)
        self.rate = str(rate)
        self.vol = str(vol)
        # Pre-processors and tokenizer
        self.pre_processor_funcs = pre_processor_funcs
        self.tokenizer_func = tokenizer_func

    def _tokenize(self, text):
        # Pre-clean
        text = text.strip()

        # Apply pre-processors
        for pp in self.pre_processor_funcs:
            logging.debug("pre-processing: %s", pp)
            text = pp(text)

        if _len(text) <= responsiveVoice.CHARACTER_LIMIT:
            return _clean_tokens([text])

        # Tokenize
        tokens = self.tokenizer_func(text)

        # Clean
        tokens = _clean_tokens(tokens)

        # Minimize
        min_tokens = []
        for t in tokens:
            min_tokens += _minimize(t, ' ', responsiveVoice.CHARACTER_LIMIT)
        return min_tokens

    def get_mp3(self,output_file="",voice_name=DEFAULT_VOICE,pitch=PITCH,rate=RATE,volume=VOL):
        '''Call the API and write to file.
        
        Args:
            output_file (string): Filename to write to.
            voice_name (string): voice name. Default is ``english_us_male``. 
                Use rvtts --lang to get all supported voices.
            pitch (float, optional): adjust pitch output. Default is ``0.5``.
            rate (float, optional): adjust rate output. Default is ``0.5``.
            vol (float, optional): adjust volume output. Default is ``1``.
        '''
        parts = self._tokenize(self.text)
        output_file = output_file or f'{hash(self.text)}.mp3'
        with open(output_file,"wb") as f:
            for p in parts:
                payload = {'t':p}
                # Update voice from user input
                payload.update(responsiveVoice.VOICE[voice_name])
                # Pitch, rate, vol from user input
                payload.update({'pitch':str(pitch),'rate':str(rate),'vol':str(volume)})
                logging.debug(payload)
                r = requests.get(responsiveVoice.API,params=payload,headers=responsiveVoice.RV_HEADER)
                f.write(r.content)

def print_voice(ctx, params, value):
    '''--lang flag.
    Print a list of supported voices.
    '''
    if not value or ctx.resilient_parsing:
        return
    click.echo('\n'.join(sorted(responsiveVoice.VOICE.keys())))
    ctx.exit()

def validate_voice(ctx, params, value):
    '''To check if user input voice is in the supported voices list.'''
    if value not in responsiveVoice.VOICE.keys():
        raise click.UsageError(f'Voice {value} is not supported!\n'
                                '-l or --lang to list all supported voices.')
    return value

def validate_pitch(ctx, params, value):
    '''To check if user input a valid pitch range.'''
    value = float(value)
    if value < 0 or value > 1:
        raise click.UsageError(f'Pitch value is not supported!\n'
                                'Valid range: 0-1')
    return value

def validate_rate(ctx, params, value):
    '''To check if user input a valid rate range.'''
    value = float(value)
    if value < 0 or value > 1:
        raise click.UsageError(f'Rate value is not supported!\n'
                                'Valid range: 0-1')
    return value

def validate_vol(ctx, params, value):
    '''To check if user input a valid rate range.'''
    value = float(value)
    if value < 0 or value > 1:
        raise click.UsageError(f'Volume value is not supported!\n'
                                'Valid range: 0-1')
    return value

def debug_mode(ctx, params, debug):
    if debug:
        format = '%(asctime)s: %(message)s'
        logging.basicConfig(format=format, level=logging.DEBUG,datefmt="%H:%M:%S")
        logging.getLogger()
    return

@click.command()
@click.option('-l','--lang', 
                is_flag=True, 
                callback=print_voice,
                expose_value=False, 
                is_eager=True,
                help='Print all supported voice.')
@click.option('-t','--text',
                type=str,
                help='Text to convert.')
@click.option('-i','--input',
                type=click.File(encoding='utf8'),
                help='Input file. For example: -i doc-ton-tam-gioi-chuong-0001.txt')
@click.option('-o','--output',
                type=click.Path(),
                required=True,
                help='Output file. For example: -o doc-ton-tam-gioi-chuong-0001.mp3')
@click.option('-v','--voice',
                default=responsiveVoice.DEFAULT_VOICE,
                required=True,
                callback=validate_voice,
                help='Output voices. For example: -v vietnamese_male')
@click.option('--pitch',
                default=responsiveVoice.PITCH,
                callback=validate_pitch,
                help='Adjust pitch (range 0 to 1). Default: 0.5')
@click.option('--rate',
                default=responsiveVoice.RATE,
                callback=validate_rate,
                help='Adjust rate (range 0 to 1). Default: 0.5')
@click.option('--volume',
                default=responsiveVoice.VOL,
                type=float,
                callback=validate_vol,
                help='Adjust volume (range 0 to 1). Default: 1')
@click.option('-d','--debug',
                is_flag=True, 
                callback=debug_mode,
                help='Debug mode.')
@click.version_option(version=__version__)
def tts(text,input,output,voice,pitch,rate,volume,debug=False):
    '''Convert text or input file to to mp3 using ResponsiveVoice's API.
    '''
    if text and input:
        raise click.UsageError('<text> and <input file> can\'t be used together!!!')
    if text:
        t = responsiveVoice(text)
        t.get_mp3(click.format_filename(output),voice,pitch=pitch,rate=rate,volume=volume)
    elif input:
        t = responsiveVoice(input.read())
        t.get_mp3(click.format_filename(output),voice,pitch=pitch,rate=rate,volume=volume)


if __name__ == "__main__":
    tts()