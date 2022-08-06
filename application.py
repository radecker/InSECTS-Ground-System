from time import strftime
from flask import Flask, render_template, request, redirect
import boto3, jinja2, os, datetime


currentDateTime=datetime.datetime.now()

counter_request_number = 1
autonomy_status = 0
fan_speed = 100
trim_position=0

def python_to_html(python_array, index_value):
    html_parameter=python_array[len(python_array)-index_value]
    return html_parameter

def read_dynamoDB(tableName, dbItems, parameter):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(tableName)

    reading = table.scan()
    reading[dbItems]

    array_msg_id=[]
    array_command_sent=[]
    array_fan_speeds=[]
    array_temperature_1=[]
    array_temperature_2=[]
    array_temperature_3=[]
    array_temperature_4=[]
    array_temperature_5=[]
    array_trimPosition=[]
    array_autonomyState=[]
    array_dates=[]
    array_times=[]

    for item in reading['Items']:
        if tableName == 'Spacecraft_Telemetry_to_Ground':
            array_msg_id.append(item['Downlink_Msg_ID'])
            array_fan_speeds.append(item['Fan_Speed'])
            array_temperature_1.append(item['Temperature_1'])
            array_temperature_2.append(item['Temperature_2'])
            array_temperature_3.append(item['Temperature_3'])
            array_temperature_4.append(item['Temperature_4'])
            array_temperature_5.append(item['Temperature_5'])
            array_trimPosition.append(item['Trim_Position'])
            array_autonomyState.append(item['Autonomy_State'])
            array_dates.append(item['Date'])
            array_times.append(item['Time'])
        if tableName == 'Ground_Commands_To_Spacecraft' or tableName == 'Ground_to_Spacecraft_Temporary_Queue':
            array_msg_id.append(item['Request_Number'])
            array_fan_speeds.append(item['Fan_Speed'])
            array_trimPosition.append(item['Trim_Position'])
            array_autonomyState.append(item['Autonomy_status'])
            array_dates.append(item['Date'])
            array_times.append(item['Time'])

        
    if parameter == 'temp1':
        return array_temperature_1
    elif parameter == 'temp2':
        return array_temperature_2
    elif parameter == 'temp3':
        return array_temperature_3
    elif parameter == 'temp4':
        return array_temperature_4
    elif parameter == 'temp5':
        return array_temperature_5
    elif parameter == 'fan':
        return array_fan_speeds
    elif parameter == 'trim':
        return array_trimPosition
    elif parameter == 'auto':
        return array_autonomyState
    elif parameter == 'date':
        return array_dates
    elif parameter == 'time':
        return array_times
    elif parameter == 'request_number':
        return array_msg_id
    elif parameter == 'command_sent':
        return array_command_sent
    
# creates Flask web application
application = Flask(__name__)

@application.route('/line_chart.html')
def line():
    downlinkTimes = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','time')
    temp1 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp1')
    temp2 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp2')
    temp3 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp3')
    temp4 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp4')
    temp5 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp5')
    
    line_labels=downlinkTimes
    line_values=temp1
    
    return render_template('line_chart.html', title='Temperature Readings from Sensor 1', min=-100, max=100, labels=line_labels, values=line_values, values2=temp2)

# home directory
@application.route('/')
def home():
    global autonomy_status
    global fan_speed
    global trim_position
    global currentDateTime
    global counter_request_number
    counter = 0

    downlinkID = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','request_number')
    temp1 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp1')
    temp2 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp2')
    temp3 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp3')
    temp4 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp4')
    temp5 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp5')
    fan=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','fan')
    trim=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','trim')
    auto=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','auto')
    downlinkDates=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','date')
    downlinkTimes=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','time')
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    # Work in Progress to create a function for simplifying the code

    # while counter <= len(temp1):
    #     counter = counter + 1
    #     return render_template('index.html', 
    #     exec('temperature1_' + str(counter) + '=python_to_html(temp1, counter)'))
    #     # exec('temperature2_' + str(counter))=python_to_html(temp2, counter),
    #     # exec('temperature3_' + str(counter))=python_to_html(temp3, counter),
    #     # exec('temperature4_' + str(counter))=python_to_html(temp4, counter),
    #     # exec('temperature5_' + str(counter))=python_to_html(temp5, counter),
    #     # exec('trimPosition_' + str(counter))=python_to_html(trim, counter),
    #     # exec('autonomyState_' + str(counter))=python_to_html(auto, counter),
    #     # exec('fanSpeed_' + str(counter))=python_to_html(fan, counter),
    #     # exec('downlinkDate_' + str(counter))=python_to_html(downlinkDates, counter),
    #     # exec('downlinkTime_' + str(counter))=python_to_html(downlinkTimes, counter))
    
    try:

        return render_template('index.html', 
        temperature1_1=temp1[len(temp1)-1],
        temperature2_1=temp2[len(temp2)-1],
        temperature3_1=temp3[len(temp3)-1],
        temperature4_1=temp4[len(temp4)-1],
        temperature5_1=temp5[len(temp5)-1],
        trimPosition_1=trim[len(trim)-1],
        autonomyState_1=auto[len(auto)-1],
        fanSpeed_1=fan[len(fan)-1],
        downlinkDate_1=downlinkDates[len(downlinkDates)-1],
        downlinkTime_1=downlinkTimes[len(downlinkTimes)-1],

        temperature_2=temp1[len(temp1)-2], 
        temperature2_2=temp2[len(temp2)-2],
        temperature3_2=temp3[len(temp3)-2],
        temperature4_2=temp4[len(temp4)-2],
        temperature5_2=temp5[len(temp5)-2],
        trimPosition_2=trim[len(trim)-2],
        autonomyState_2=auto[len(auto)-2],
        fanSpeed_2=fan[len(fan)-2],
        downlinkDate_2=downlinkDates[len(downlinkDates)-2],
        downlinkTime_2=downlinkTimes[len(downlinkTimes)-2],

        temperature1_3=temp1[len(temp1)-3], 
        temperature2_3=temp2[len(temp2)-3],
        temperature3_3=temp3[len(temp3)-3],
        temperature4_3=temp4[len(temp4)-3],
        temperature5_3=temp5[len(temp5)-3],
        trimPosition_3=trim[len(trim)-3],
        autonomyState_3=auto[len(auto)-3],
        fanSpeed_3=fan[len(fan)-3],
        downlinkDate_3=downlinkDates[len(downlinkDates)-3],
        downlinkTime_3=downlinkTimes[len(downlinkTimes)-3],

        temperature1_4=temp1[len(temp1)-4], 
        temperature2_4=temp2[len(temp2)-4],
        temperature3_4=temp3[len(temp3)-4],
        temperature4_4=temp4[len(temp4)-4],
        temperature5_4=temp5[len(temp5)-4],
        trimPosition_4=trim[len(trim)-4],
        autonomyState_4=auto[len(auto)-4],
        fanSpeed_4=fan[len(fan)-4],
        downlinkDate_4=downlinkDates[len(downlinkDates)-4],
        downlinkTime_4=downlinkTimes[len(downlinkTimes)-4],

        # temperature1_5=temp1[len(temp1)-5], 
        # temperature2_5=temp2[len(temp2)-5],
        # temperature3_5=temp3[len(temp3)-5],
        # temperature4_5=temp4[len(temp4)-5],
        # temperature5_5=temp5[len(temp5)-5],
        # trimPosition_5=trim[len(trim)-5],
        # autonomyState_5=auto[len(auto)-5],
        # fanSpeed_5=fan[len(fan)-5],
        # downlinkDate_5=downlinkDates[len(downlinkDates)-5],
        # downlinkTime_5=downlinkTimes[len(downlinkTimes)-5],

        # temperature1_6=temp1[len(temp1)-6], 
        # temperature2_6=temp2[len(temp2)-6],
        # temperature3_6=temp3[len(temp3)-6],
        # temperature4_6=temp4[len(temp4)-6],
        # temperature5_6=temp5[len(temp5)-6],
        # trimPosition_6=trim[len(trim)-6],
        # autonomyState_6=auto[len(auto)-6],
        # fanSpeed_6=fan[len(fan)-6],
        # downlinkDate_6=downlinkDates[len(downlinkDates)-6],
        # downlinkTime_6=downlinkTimes[len(downlinkTimes)-6],

        # temperature1_7=temp1[len(temp1)-7], 
        # temperature2_7=temp2[len(temp2)-7],
        # temperature3_7=temp3[len(temp3)-7],
        # temperature4_7=temp4[len(temp4)-7],
        # temperature5_7=temp5[len(temp5)-7],
        # trimPosition_7=trim[len(trim)-7],
        # autonomyState_7=auto[len(auto)-7],
        # fanSpeed_7=fan[len(fan)-7],
        # downlinkDate_7=downlinkDates[len(downlinkDates)-7],
        # downlinkTime_7=downlinkTimes[len(downlinkTimes)-7],

        # temperature1_8=temp1[len(temp1)-8], 
        # temperature2_8=temp2[len(temp2)-8],
        # temperature3_8=temp3[len(temp3)-8],
        # temperature4_8=temp4[len(temp4)-8],
        # temperature5_8=temp5[len(temp5)-8],
        # trimPosition_8=trim[len(trim)-8],
        # autonomyState_8=auto[len(auto)-8],
        # fanSpeed_8=fan[len(fan)-8],
        # downlinkDate_8=downlinkDates[len(downlinkDates)-8],
        # downlinkTime_8=downlinkTimes[len(downlinkTimes)-8],

        # temperature1_9=temp1[len(temp1)-9], 
        # temperature2_9=temp2[len(temp2)-9],
        # temperature3_9=temp3[len(temp3)-9],
        # temperature4_9=temp4[len(temp4)-9],
        # temperature5_9=temp5[len(temp5)-9],
        # trimPosition_9=trim[len(trim)-9],
        # autonomyState_9=auto[len(auto)-9],
        # fanSpeed_9=fan[len(fan)-9],
        # downlinkDate_9=downlinkDates[len(downlinkDates)-9],
        # downlinkTime_9=downlinkTimes[len(downlinkTimes)-9],

        # temperature1_10=temp1[len(temp1)-10], 
        # temperature2_10=temp2[len(temp2)-10],
        # temperature3_10=temp3[len(temp3)-10],
        # temperature4_10=temp4[len(temp4)-10],
        # temperature5_10=temp5[len(temp5)-10],
        # trimPosition_10=trim[len(trim)-10],
        # autonomyState_10=auto[len(auto)-10],
        # fanSpeed_10=fan[len(fan)-10],
        # downlinkDate_10=downlinkDates[len(downlinkDates)-10],
        # downlinkTime_10=downlinkTimes[len(downlinkTimes)-10],
        )
    except:
        return render_template('index.html')

# home directory alternative url
@application.route('/index.html')
def index():
    return home()

# login screen (not functional at this time)
@application.route('/login.html')
def login():
    return render_template('login.html')

# password screen (not functional at this time)
@application.route('/password.html')
def password():
    return render_template('password.html')

# account registration screen (not functional at this time)
@application.route('/register.html')
def register():
    return render_template('register.html')

# pulls data from thermal database to make charts
@application.route('/thermal-history.html')
def historicData():
    return render_template('thermal-history.html')

# table that pulls data from thermal database
@application.route('/thermal-database.html')
def thermalDatabase():
    global autonomy_status
    global fan_speed
    global trim_position
    global currentDateTime
    global counter_request_number

    	
    downlinkID = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','downlinkID')
    temp1 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp1')
    temp2 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp2')
    temp3 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp3')
    temp4 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp4')
    temp5 = read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','temp5')
    fan=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','fan')
    trim=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','trim')
    auto=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','auto')
    downlinkDates=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','date')
    downlinkTimes=read_dynamoDB('Spacecraft_Telemetry_to_Ground', 'Items','time')
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    try:

        return render_template('thermal-database.html', 
        
        temperature1_1=temp1[len(temp1)-1], 
        temperature2_1=temp2[len(temp2)-1],
        temperature3_1=temp3[len(temp3)-1],
        temperature4_1=temp4[len(temp4)-1],
        temperature5_1=temp5[len(temp5)-1],
        trimPosition_1=trim[len(trim)-1],
        autonomyState_1=auto[len(auto)-1],
        fanSpeed_1=fan[len(fan)-1],
        downlinkDate_1=downlinkDates[len(downlinkDates)-1],
        downlinkTime_1=downlinkTimes[len(downlinkTimes)-1],

        temperature_2=temp1[len(temp1)-2], 
        temperature2_2=temp2[len(temp2)-2],
        temperature3_2=temp3[len(temp3)-2],
        temperature4_2=temp4[len(temp4)-2],
        temperature5_2=temp5[len(temp5)-2],
        trimPosition_2=trim[len(trim)-2],
        autonomyState_2=auto[len(auto)-2],
        fanSpeed_2=fan[len(fan)-2],
        downlinkDate_2=downlinkDates[len(downlinkDates)-2],
        downlinkTime_2=downlinkTimes[len(downlinkTimes)-2],

        temperature1_3=temp1[len(temp1)-3], 
        temperature2_3=temp2[len(temp2)-3],
        temperature3_3=temp3[len(temp3)-3],
        temperature4_3=temp4[len(temp4)-3],
        temperature5_3=temp5[len(temp5)-3],
        trimPosition_3=trim[len(trim)-3],
        autonomyState_3=auto[len(auto)-3],
        fanSpeed_3=fan[len(fan)-3],
        downlinkDate_3=downlinkDates[len(downlinkDates)-3],
        downlinkTime_3=downlinkTimes[len(downlinkTimes)-3],

        temperature1_4=temp1[len(temp1)-4], 
        temperature2_4=temp2[len(temp2)-4],
        temperature3_4=temp3[len(temp3)-4],
        temperature4_4=temp4[len(temp4)-4],
        temperature5_4=temp5[len(temp5)-4],
        trimPosition_4=trim[len(trim)-4],
        autonomyState_4=auto[len(auto)-4],
        fanSpeed_4=fan[len(fan)-4],
        downlinkDate_4=downlinkDates[len(downlinkDates)-4],
        downlinkTime_4=downlinkTimes[len(downlinkTimes)-4],

        # temperature1_5=temp1[len(temp1)-5], 
        # temperature2_5=temp2[len(temp2)-5],
        # temperature3_5=temp3[len(temp3)-5],
        # temperature4_5=temp4[len(temp4)-5],
        # temperature5_5=temp5[len(temp5)-5],
        # trimPosition_5=trim[len(trim)-5],
        # autonomyState_5=auto[len(auto)-5],
        # fanSpeed_5=fan[len(fan)-5],
        # downlinkDate_5=downlinkDates[len(downlinkDates)-5],
        # downlinkTime_5=downlinkTimes[len(downlinkTimes)-5],

        # temperature1_6=temp1[len(temp1)-6], 
        # temperature2_6=temp2[len(temp2)-6],
        # temperature3_6=temp3[len(temp3)-6],
        # temperature4_6=temp4[len(temp4)-6],
        # temperature5_6=temp5[len(temp5)-6],
        # trimPosition_6=trim[len(trim)-6],
        # autonomyState_6=auto[len(auto)-6],
        # fanSpeed_6=fan[len(fan)-6],
        # downlinkDate_6=downlinkDates[len(downlinkDates)-6],
        # downlinkTime_6=downlinkTimes[len(downlinkTimes)-6],

        # temperature1_7=temp1[len(temp1)-7], 
        # temperature2_7=temp2[len(temp2)-7],
        # temperature3_7=temp3[len(temp3)-7],
        # temperature4_7=temp4[len(temp4)-7],
        # temperature5_7=temp5[len(temp5)-7],
        # trimPosition_7=trim[len(trim)-7],
        # autonomyState_7=auto[len(auto)-7],
        # fanSpeed_7=fan[len(fan)-7],
        # downlinkDate_7=downlinkDates[len(downlinkDates)-7],
        # downlinkTime_7=downlinkTimes[len(downlinkTimes)-7],

        # temperature1_8=temp1[len(temp1)-8], 
        # temperature2_8=temp2[len(temp2)-8],
        # temperature3_8=temp3[len(temp3)-8],
        # temperature4_8=temp4[len(temp4)-8],
        # temperature5_8=temp5[len(temp5)-8],
        # trimPosition_8=trim[len(trim)-8],
        # autonomyState_8=auto[len(auto)-8],
        # fanSpeed_8=fan[len(fan)-8],
        # downlinkDate_8=downlinkDates[len(downlinkDates)-8],
        # downlinkTime_8=downlinkTimes[len(downlinkTimes)-8],

        # temperature1_9=temp1[len(temp1)-9], 
        # temperature2_9=temp2[len(temp2)-9],
        # temperature3_9=temp3[len(temp3)-9],
        # temperature4_9=temp4[len(temp4)-9],
        # temperature5_9=temp5[len(temp5)-9],
        # trimPosition_9=trim[len(trim)-9],
        # autonomyState_9=auto[len(auto)-9],
        # fanSpeed_9=fan[len(fan)-9],
        # downlinkDate_9=downlinkDates[len(downlinkDates)-9],
        # downlinkTime_9=downlinkTimes[len(downlinkTimes)-9],

        # temperature1_10=temp1[len(temp1)-10], 
        # temperature2_10=temp2[len(temp2)-10],
        # temperature3_10=temp3[len(temp3)-10],
        # temperature4_10=temp4[len(temp4)-10],
        # temperature5_10=temp5[len(temp5)-10],
        # trimPosition_10=trim[len(trim)-10],
        # autonomyState_10=auto[len(auto)-10],
        # fanSpeed_10=fan[len(fan)-10],
        # downlinkDate_10=downlinkDates[len(downlinkDates)-10],
        # downlinkTime_10=downlinkTimes[len(downlinkTimes)-10],
        )
    except:
        return render_template('thermal-database.html')

# ground segment log

@application.route('/ground-segment-log.html')
def groundSegmentLog():
    global autonomy_status
    global fan_speed
    global trim_position
    global currentDateTime
    global counter_request_number
    global currentDateTime

    msgId = read_dynamoDB('Ground_Commands_To_Spacecraft', 'Items','request_number')
    commandSent = read_dynamoDB('Ground_Commands_To_Spacecraft', 'Items', 'command_sent')
    fan=read_dynamoDB('Ground_Commands_To_Spacecraft', 'Items','fan')
    trim=read_dynamoDB('Ground_Commands_To_Spacecraft', 'Items','trim')
    auto=read_dynamoDB('Ground_Commands_To_Spacecraft', 'Items','auto')
    uplinkDates=read_dynamoDB('Ground_Commands_To_Spacecraft', 'Items','date')
    uplinkTimes=read_dynamoDB('Ground_Commands_To_Spacecraft', 'Items','time')
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    return render_template('ground-segment-log.html', 
    
    request_number_1=msgId[len(msgId)-1], 
    command_sent_1=commandSent[len(commandSent)-1],
    trim_position_1=trim[len(trim)-1],
    autonomy_status_1=auto[len(auto)-1],
    fan_speed_1=fan[len(fan)-1],
    date_1=uplinkDates[len(uplinkDates)-1],
    time_1=uplinkTimes[len(uplinkTimes)-1],

    request_number_2=msgId[len(msgId)-2], 
    command_sent_2=commandSent[len(commandSent)-2],
    trim_position_2=trim[len(trim)-2],
    autonomy_status_2=auto[len(auto)-2],
    fan_speed_2=fan[len(fan)-2],
    date_2=uplinkDates[len(uplinkDates)-2],
    time_2=uplinkTimes[len(uplinkTimes)-2],

    request_number_3=msgId[len(msgId)-3], 
    command_sent_3=commandSent[len(commandSent)-3],
    trim_position_3=trim[len(trim)-3],
    autonomy_status_3=auto[len(auto)-3],
    fan_speed_3=fan[len(fan)-3],
    date_3=uplinkDates[len(uplinkDates)-3],
    time_3=uplinkTimes[len(uplinkTimes)-3],

    request_number_4=msgId[len(msgId)-4], 
    command_sent_4=commandSent[len(commandSent)-4],
    trim_position_4=trim[len(trim)-4],
    autonomy_status_4=auto[len(auto)-4],
    fan_speed_4=fan[len(fan)-4],
    date_4=uplinkDates[len(uplinkDates)-4],
    time_4=uplinkTimes[len(uplinkTimes)-4],

    request_number_5=msgId[len(msgId)-5], 
    command_sent_5=commandSent[len(commandSent)-5],
    trim_position_5=trim[len(trim)-5],
    autonomy_status_5=auto[len(auto)-5],
    fan_speed_5=fan[len(fan)-5],
    date_5=uplinkDates[len(uplinkDates)-5],
    time_5=uplinkTimes[len(uplinkTimes)-5],

    request_number_6=msgId[len(msgId)-6], 
    command_sent_6=commandSent[len(commandSent)-6],
    trim_position_6=trim[len(trim)-6],
    autonomy_status_6=auto[len(auto)-6],
    fan_speed_6=fan[len(fan)-6],
    date_6=uplinkDates[len(uplinkDates)-6],
    time_6=uplinkTimes[len(uplinkTimes)-6],

    request_number_7=msgId[len(msgId)-7], 
    command_sent_7=commandSent[len(commandSent)-7],
    trim_position_7=trim[len(trim)-7],
    autonomy_status_7=auto[len(auto)-7],
    fan_speed_7=fan[len(fan)-7],
    date_7=uplinkDates[len(uplinkDates)-7],
    time_7=uplinkTimes[len(uplinkTimes)-7],

    request_number_8=msgId[len(msgId)-8], 
    command_sent_8=commandSent[len(commandSent)-8],
    trim_position_8=trim[len(trim)-8],
    autonomy_status_8=auto[len(auto)-8],
    fan_speed_8=fan[len(fan)-8],
    date_8=uplinkDates[len(uplinkDates)-8],
    time_8=uplinkTimes[len(uplinkTimes)-8],

    request_number_9=msgId[len(msgId)-9], 
    command_sent_9=commandSent[len(commandSent)-9],
    trim_position_9=trim[len(trim)-9],
    autonomy_status_9=auto[len(auto)-9],
    fan_speed_9=fan[len(fan)-9],
    date_9=uplinkDates[len(uplinkDates)-9],
    time_9=uplinkTimes[len(uplinkTimes)-9],

    request_number_10=msgId[len(msgId)-10], 
    command_sent_10=commandSent[len(commandSent)-10],
    trim_position_10=trim[len(trim)-10],
    autonomy_status_10=auto[len(auto)-10],
    fan_speed_10=fan[len(fan)-10],
    date_10=uplinkDates[len(uplinkDates)-10],
    time_10=uplinkTimes[len(uplinkTimes)-10],
    )
    
# ground segment status (not functional at this time)
@application.route('/ground-segment-status.html')
def groundSegmentStatus():
    return render_template('ground-segment-status.html')

# command request form - autonomy mode is off
@application.route('/commands-manual.html', methods=['GET','POST'])
def commandsManualOn():
    global autonomy_status
    global fan_speed
    global trim_position
    global currentDateTime
    global counter_request_number

    # msgId = read_dynamoDB('Ground_to_Spacecraft_Temporary_Queue', 'Items','request_number')
    # fan=read_dynamoDB('Ground_to_Spacecraft_Temporary_Queue', 'Items','fan')
    # trim=read_dynamoDB('Ground_to_Spacecraft_Temporary_Queue', 'Items','trim')
    # auto=read_dynamoDB('Ground_to_Spacecraft_Temporary_Queue', 'Items','auto')
    # uplinkDates=read_dynamoDB('Ground_to_Spacecraft_Temporary_Queue', 'Items','date')
    # uplinkTimes=read_dynamoDB('Ground_to_Spacecraft_Temporary_Queue', 'Items','time')


    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(name='Ground_Commands_To_Spacecraft')
    queue = dynamodb.Table(name='Ground_to_Spacecraft_Temporary_Queue')

    if request.method == 'POST':
        currentDateTime=datetime.datetime.now()
        # Trim position toggle
        if request.form['submit_button'] == 'trimpos':
            if trim_position == 0:
                trim_position = 1
            elif trim_position == 1:
                trim_position = 2
            else:
                trim_position =0
            response = table.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Trim_Position': str(trim_position)
                    }
                )
            addToQueue = queue.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Trim_Position': str(trim_position),
                    }
                )
            counter_request_number=counter_request_number + 1 
            return redirect(f"/commands-manual.html")
        # Autonomy state turns from 0 to 1
        elif request.form['submit_button']=='autonomyon':
            autonomy_status = 1
            response = table.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Autonomy_status': str(autonomy_status)
                    }
                )
            addToQueue = queue.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Autonomy_status': str(autonomy_status)
                    }
                )
            counter_request_number=counter_request_number + 1 
            return redirect(f"/autonomy-mode-commands.html")
        # Fan speed command
        else:
            fan_speed = request.form['submit_button']
            response = table.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Fan_Speed': fan_speed
                }
            )
            addToQueue = queue.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Fan_Speed': fan_speed
                }
             )
            print("Fan speed is "+ str(fan_speed))
            counter_request_number=counter_request_number + 1 
            return redirect(f"/commands-manual.html") 
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    return render_template('commands-manual.html'
    # ,
    # request_number_1=msgId[len(msgId)-1],
    # trim_position_1=trim[len(trim)-1],
    # autonomy_status_1=auto[len(auto)-1],
    # fan_speed_1=fan[len(fan)-1],
    # date_1=uplinkDates[len(uplinkDates)-1],
    # time_1=uplinkTimes[len(uplinkTimes)-1],
    )

# command request form - manual mode is OFF
@application.route('/autonomy-mode-commands.html', methods=['GET','POST'])
def autoCommands():
    global autonomy_status
    global fan_speed
    global trim_position
    global currentDateTime
    global counter_request_number

    currentDateTime=datetime.datetime.now()

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(name='Ground_Commands_To_Spacecraft')
    queue = dynamodb.Table(name='Ground_to_Spacecraft_Temporary_Queue')
       
    if request.method == 'POST':
        # Autonomy state turns from 1 to 0
        if request.form['submit_button']=='autonomyon':
            autonomy_status = 0
            print(str(autonomy_status))
            response = table.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Autonomy_status': str(autonomy_status)
                    }
                )
            addToQueue = queue.put_item(
                Item={
                    'Request_Number': str(counter_request_number),
                    'Date': str(currentDateTime.date()),
                    'Time': str(currentDateTime.time()),
                    'Autonomy_status': str(autonomy_status)
                    }
                )
            counter_request_number=counter_request_number + 1
            return redirect(f"/commands-manual.html")

    
    
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    if autonomy_status==1:
        return render_template('autonomy-mode-commands.html')
    else:
        return render_template('commands-manual.html')


# about the project
@application.route('/about-insects.html')
def aboutInsects():
    return render_template('about-insects.html')

# about the team
@application.route('/about-the-team.html')
def abouttheteam():
    return render_template('about-the-team.html')

if __name__=="__main__":
    application.run(debug=True)

