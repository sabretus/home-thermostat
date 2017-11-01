import remi.gui as gui
from remi import start, App
from ConfigParser import SafeConfigParser
from updatetmp import updatetmp
from subprocess import call

config_path = '/tmp/config.ini'

def update_config(key, value):
    config = SafeConfigParser()
    config.read(config_path)
    config.set('main', key, value)
    with open(config_path, 'w') as f:
        config.write(f)

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=300, height=350, margin='0px auto')

        templist = [ '16 C*', '17 C*', '18 C*', '19 C*', '20 C*', '21 C*', '22 C*', '23 C*' ]
        timelistNightBegin = [ '01:00',  '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00' ]
        timelistNightEnd = [ '01:00',  '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00' ]
        timelistDayBegin = [ '13:00',  '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '00:00' ]
        timelistDayEnd = [ '13:00',  '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '00:00' ]

        config = SafeConfigParser()
        config.read(config_path)

        self.bt = gui.Label('Home thermostat settings')

        self.lblFurnace = gui.Label('Manual furnace control (Warning!)')
        self.lbl = gui.Label('Temperature: ' + config.get('main', 'temp'))
        self.lblNight = gui.Label('Evening timeslot: ' + config.get('main', 'timeslotdaybegin') + '-' + config.get('main', 'timeslotdayend'))
        self.lblDay = gui.Label('Morning timeslot: ' + config.get('main', 'timeslotnightbegin') + '-' + config.get('main', 'timeslotnightend'))

        self.dropDownFurnace = gui.DropDown.new_from_list(('Turn ON', 'Turn OFF'), width=100, height=20, margin='10px')
        self.dropDownFurnace.set_on_change_listener(self.drop_down_changed_state)
        self.dropDownFurnace.select_by_value('Turn OFF')

        self.dropDown = gui.DropDown.new_from_list((templist), width=100, height=20, margin='10px')
        self.dropDown.set_on_change_listener(self.drop_down_changed_temp)
        self.dropDown.select_by_value('20 C*')

        self.dropDownTimeBegin1 = gui.DropDown.new_from_list((timelistDayBegin), width=100, height=20)
        self.dropDownTimeBegin1.set_on_change_listener(self.drop_down_changed_time_day_begin)
        self.dropDownTimeEnd1 = gui.DropDown.new_from_list((timelistDayEnd), width=100, height=20)
        self.dropDownTimeEnd1.set_on_change_listener(self.drop_down_changed_time_day_end)

        self.dropDownTimeBegin2 = gui.DropDown.new_from_list((timelistNightBegin), width=100, height=20)
        self.dropDownTimeBegin2.set_on_change_listener(self.drop_down_changed_time_night_begin)
        self.dropDownTimeEnd2 = gui.DropDown.new_from_list((timelistNightEnd), width=100, height=20)
        self.dropDownTimeEnd2.set_on_change_listener(self.drop_down_changed_time_night_end)

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
        call (["relay_off.py"])
        updatetmp(config_path)

    def drop_down_changed_state(self, widget, value):
        if value == 'Turn ON':
            call (["relay_on.py"])
            self.bt.set_text('WARNING!!!, HEATING ENABLED MANUALLY')
        else:
            call (["relay_off.py"])
            self.bt.set_text('Heating turned off manually')

    def drop_down_changed_time_day_begin(self, widget, value):
        update_config('timeslotdaybegin', value)
        self.bt.set_text('Morning heating will begin at: ' + value)
        updatetmp(config_path)

    def drop_down_changed_time_day_end(self, widget, value):
        update_config('timeslotdayend', value)
        self.bt.set_text('Morning heating will end at: ' + value)
        updatetmp(config_path)

    def drop_down_changed_time_night_begin(self, widget, value):
        update_config('timeslotnightbegin', value)
        self.bt.set_text('Evenening heating will begin at: ' + value)
        updatetmp(config_path)

    def drop_down_changed_time_night_end(self, widget, value):
        update_config('timeslotnightend', value)
        self.bt.set_text('Evenening heating will end at: ' + value)
        updatetmp(config_path)

# starts the webserver
start(MyApp, address='0.0.0.0', start_browser=False)
