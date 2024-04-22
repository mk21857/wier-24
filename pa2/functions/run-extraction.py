import sys
import regex
import os


script_dir = os.path.dirname(os.path.realpath(__file__))

html_overstock_jewelery1_path = os.path.join(script_dir,
                                             '../pages/overstock.com/jewelry01.html')
html_overstock_jewelery2_path = os.path.join(script_dir,
                                             '../pages/overstock.com/jewelry02.html')
html_rtv_audi_path = os.path.join(script_dir,
                                  '../pages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html')
html_rtv_volvo_path = os.path.join(script_dir,
                                   '../pages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html')
sport_tv_doncic_1_path = os.path.join(script_dir,
                                        '../pages/sport-tv.si/doncic-in-dallas-izgubili-prvo-tekmo-koncnice-v-kaliforniji.html')
sport_tv_doncic_2_path = os.path.join(script_dir,
                                        '../pages/sport-tv.si/doncic-med-tremi-finalisti-za-naziv-mvp-ja-lige-nba.html')
bolha_avto_oglasi_mercedes_path = os.path.join(script_dir,
                                                  '../pages/bolha.com/avto-oglasimercedes.html')
bolha_avto_oglasi_renault_path = os.path.join(script_dir,
                                                  '../pages/bolha.com/avto-oglasirenault.html')

html_overstock_jewelery1 = open(html_overstock_jewelery1_path).read()
html_overstock_jewelery2 = open(html_overstock_jewelery2_path).read()
html_rtv_audi = open(html_rtv_audi_path, encoding='utf-8').read()
html_rtv_volvo = open(html_rtv_volvo_path, encoding='utf-8').read()
html_sport_tv_doncic_1 = open(sport_tv_doncic_1_path, encoding='utf-8').read()
html_sport_tv_doncic_2 = open(sport_tv_doncic_2_path, encoding='utf-8').read()
bolha_avto_oglasi_mercedes = open(bolha_avto_oglasi_mercedes_path, encoding='utf-8').read()
bolha_avto_oglasi_renault = open(bolha_avto_oglasi_renault_path, encoding='utf-8').read()


algo = sys.argv[1]

if algo == 'A':
    print('OVERSTOCK 1', regex.overstock(html_overstock_jewelery1), end='\n\n')
    print('OVERSTOCK 2',regex.overstock(html_overstock_jewelery2), end='\n\n')
    print('RTVSLO 1', regex.rtv(html_rtv_audi), end='\n\n')
    print('RTVSLO 2', regex.rtv(html_rtv_volvo), end='\n\n')
    print('SPORT-TV 1', regex.sport_tv(html_sport_tv_doncic_1), end='\n\n')
    print('SPORT-TV 2', regex.sport_tv(html_sport_tv_doncic_2), end='\n\n')
    print('BOLHA 1', regex.bolha(bolha_avto_oglasi_mercedes), end='\n\n')
    print('BOLHA 2', regex.bolha(bolha_avto_oglasi_renault), end='\n\n')
elif algo == 'B':
    print('')
elif algo == 'C':
    print('')
