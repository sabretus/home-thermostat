import configparser
import subprocess

import remi.gui as gui
from remi import App, start

from updatetemp import updatetmp

# config_path = '/opt/remiui/config.ini'
config_path = 'config.ini'
furnace_api = 'http://192.168.0.99/api/relay2'
furnace_turn_on = "/usr/bin/wget -q --post-data 'state=1' -O - " + furnace_api
furnace_turn_off = "/usr/bin/wget -q --post-data 'state=0' -O - " + furnace_api


def update_config(key, value):
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set('main', key, value)
    with open(config_path, 'w') as f:
        config.write(f)


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=300, height=350, margin='0px auto')

        templist = [
            '16 °C', '17 °C', '18 °C', '19 °C', '20 °C',
            '21 °C', '21.2 °C', '21.4 °C', '21.6 °C', '21.8 °C',
            '22 °C', '22.2 °C', '22.4 °C', '22.6 °C', '22.8 °C',
            '23 °C', '23.2 °C', '23.4 °C', '23.6 °C', '23.8 °C'
        ]
        timelistNightBegin = ['01:00',  '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00']
        timelistNightEnd = ['01:00',  '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00']
        timelistDayBegin = ['13:00',  '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '00:00']
        timelistDayEnd = ['13:00',  '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '00:00']

        config = configparser.ConfigParser()
        config.read(config_path)

        self.bt = gui.Label('HOME THERMOSTAT SETTINGS')

        config.get('main', 'timeslotdaybegin')

        self.lblFurnace = gui.Label('Manual furnace control (Warning!)')
        self.lbl = gui.Label('Temperature:')
        self.lblNight = gui.Label('Evening timeslot:')
        self.lblDay = gui.Label('Morning timeslot:')

        self.dropDownFurnace = gui.DropDown.new_from_list(('Turn ON', 'Turn OFF'), width=100, height=20, margin='10px')
        self.dropDownFurnace.set_on_change_listener(self.drop_down_changed_state)
        self.dropDownFurnace.select_by_value('Turn OFF')

        self.dropDown = gui.DropDown.new_from_list((templist), width=100, height=20, margin='10px')
        self.dropDown.set_on_change_listener(self.drop_down_changed_temp)
        self.dropDown.select_by_value(config.get('main', 'temp'))

        # evening timeslot
        self.dropDownTimeBegin1 = gui.DropDown.new_from_list((timelistDayBegin), width=100, height=20)
        self.dropDownTimeBegin1.set_on_change_listener(self.drop_down_changed_time_day_begin)
        self.dropDownTimeBegin1.select_by_value(config.get('main', 'timeslotdaybegin'))
        self.dropDownTimeEnd1 = gui.DropDown.new_from_list((timelistDayEnd), width=100, height=20)
        self.dropDownTimeEnd1.set_on_change_listener(self.drop_down_changed_time_day_end)
        self.dropDownTimeEnd1.select_by_value(config.get('main', 'timeslotdayend'))

        # morning timeslot
        self.dropDownTimeBegin2 = gui.DropDown.new_from_list((timelistNightBegin), width=100, height=20)
        self.dropDownTimeBegin2.set_on_change_listener(self.drop_down_changed_time_night_begin)
        self.dropDownTimeBegin2.select_by_value(config.get('main', 'timeslotnightbegin'))
        self.dropDownTimeEnd2 = gui.DropDown.new_from_list((timelistNightEnd), width=100, height=20)
        self.dropDownTimeEnd2.set_on_change_listener(self.drop_down_changed_time_night_end)
        self.dropDownTimeEnd2.select_by_value(config.get('main', 'timeslotnightend'))

        # appending a widget to another, the first argument is a string key
        container.append(self.bt)
        container.append(self.lbl)
        container.append(self.dropDown)
        container.append(self.lblDay)
        container.append(self.dropDownTimeBegin2)
        container.append(self.dropDownTimeEnd2)
        container.append(self.lblNight)
        container.append(self.dropDownTimeBegin1)
        container.append(self.dropDownTimeEnd1)
        container.append(self.lblFurnace)
        container.append(self.dropDownFurnace)

        # returning the root widget
        return container

    def drop_down_changed_temp(self, widget, value):
        update_config('temp', value)
        self.bt.set_text('Home temperature set to: ' + value)
        subprocess.call(furnace_turn_off, shell=True)
        updatetmp(config_path)

    def drop_down_changed_state(self, widget, value):
        if value == 'Turn ON':
            subprocess.call(furnace_turn_on, shell=True)
            self.bt.set_text('WARNING!!!, HEATING ENABLED MANUALLY')
        else:
            subprocess.call(furnace_turn_off, shell=True)
            self.bt.set_text('Heating turned off manually')

    def drop_down_changed_time_day_begin(self, widget, value):
        update_config('timeslotdaybegin', value)
        self.bt.set_text('Evenening heating will begin at: ' + value)
        updatetmp(config_path)

    def drop_down_changed_time_day_end(self, widget, value):
        update_config('timeslotdayend', value)
        self.bt.set_text('Evenening heating will end at: ' + value)
        updatetmp(config_path)

    def drop_down_changed_time_night_begin(self, widget, value):
        update_config('timeslotnightbegin', value)
        self.bt.set_text('Morning heating will begin at: ' + value)
        updatetmp(config_path)

    def drop_down_changed_time_night_end(self, widget, value):
        update_config('timeslotnightend', value)
        self.bt.set_text('Morning heating will end at: ' + value)
        updatetmp(config_path)


# starts the webserver
start(MyApp, address='0.0.0.0', port=8082, start_browser=False, username='user', password='shara123')
# start(MyApp, debug=True, address='0.0.0.0', port=8081,
#       start_browser=True, multiple_instance=True,
#       username='user', password='shara123')

