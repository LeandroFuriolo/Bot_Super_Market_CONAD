from booking.booking import Booking
from time import sleep


# inside booking ourself can be make teardown=Fale
# to close google chrome or teardown=True ro mantein opened
# when the script are finished "Boocking(teardown=True/False)"

try:
    with Booking() as bot:
        #bot.validator()
        bot.land_first_page('https://spesaonline.conad.it/offerte')
        bot.cookies()
        bot.offerte_per_tutti()
        bot.ordina_e_ritira()
        bot.CAP('Via Calabria')
        bot.city_clickeable('1')
        bot.select_city()
        bot.offerte_per_tutti_in_portal()
        bot.report_list()
        bot.report_save('html_table')
        bot.report_save('file_table')
        sleep(1)
except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run bot from command line \n'
            'Please add PATH of your Selenium Driver \n'
            'Windows: \n'
            '       set PATH=%PATH%;C:path_to_your_folder \n \n'   
            'Linux: \n'
            '       set PATH=%PATH%;/path/to_your/folder/ \n \n'        
            )
    else:
        raise
