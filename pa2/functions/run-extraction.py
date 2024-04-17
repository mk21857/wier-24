import sys
import regex
import os


script_dir = os.path.dirname(os.path.realpath(__file__))


html_rtv_audi_path = os.path.join(script_dir,
                                  '../pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html')
html_rtv_volvo_path = os.path.join(script_dir,
                                   '../pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html')

html_rtv_audi = open(html_rtv_audi_path, encoding='utf-8').read()
html_rtv_volvo = open(html_rtv_volvo_path, encoding='utf-8').read()

algo = sys.argv[1]

if algo == 'A':
    print(regex.rtv(html_rtv_audi))
    print(regex.rtv(html_rtv_volvo))
elif algo == 'B':
    print('')
elif algo == 'C':
    print('')