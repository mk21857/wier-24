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

html_overstock_jewelery1 = open(html_overstock_jewelery1_path).read()
html_overstock_jewelery2 = open(html_overstock_jewelery2_path).read()
html_rtv_audi = open(html_rtv_audi_path, encoding='utf-8').read()
html_rtv_volvo = open(html_rtv_volvo_path, encoding='utf-8').read()
html_sport_tv_doncic_1 = open(sport_tv_doncic_1_path, encoding='utf-8').read()
html_sport_tv_doncic_2 = open(sport_tv_doncic_2_path, encoding='utf-8').read()


algo = sys.argv[1]

if algo == 'A':
    # print(regex.overstock(html_overstock_jewelery1))
    # print(regex.overstock(html_overstock_jewelery2))
    # print(regex.rtv(html_rtv_audi))
    # print(regex.rtv(html_rtv_volvo))
    print(regex.sport_tv(html_sport_tv_doncic_1))
    # print(regex.sport_tv(html_sport_tv_doncic_2))
elif algo == 'B':
    print('')
elif algo == 'C':
    print('')
