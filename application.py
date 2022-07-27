from email.mime import application
from flask import Flask, render_template
import boto3, jinja2, os

counter_request_number = 0


application = Flask(__name__)

@application.route('/')
def home():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Spacecraft_Telemetry_to_Ground')
   
    reading=table.scan()
    reading['Items']
    array_downlink_msg_id=[]
    array_fan_speeds=[]
    array_temperature_1=[]
    for item in reading['Items']:
        array_downlink_msg_id.append(item['Downlink_Msg_ID'])
        array_fan_speeds.append(item['Fan_Speed'])
        array_temperature_1.append(item['Temperature_1'])
        
    print(array_fan_speeds)
    
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    return render_template('index.html', temperature1=array_temperature_1[0], fanSpeed=array_fan_speeds[0])

@application.route('/index.html')
def index():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Spacecraft_Telemetry_to_Ground')
   
    reading=table.scan()
    reading['Items']
    array_downlink_msg_id=[]
    array_fan_speeds=[]
    array_temperature_1=[]
    for item in reading['Items']:
        array_downlink_msg_id.append(item['Downlink_Msg_ID'])
        array_fan_speeds.append(item['Fan_Speed'])
        array_temperature_1.append(item['Temperature_1'])
        
    print(array_fan_speeds)
    
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    return render_template('index.html', temperature1=array_temperature_1[0], fanSpeed=array_fan_speeds[0])

@application.route('/login.html')
def login():
    return render_template('login.html')

@application.route('/password.html')
def password():
    return render_template('password.html')

@application.route('/register.html')
def register():
    return render_template('register.html')

@application.route('/thermal-history.html')
def historicData():
    return render_template('thermal-history.html')

@application.route('/thermal-database.html')
def thermalDatabase():
    return render_template('thermal-database.html')

@application.route('/ground-segment-log.html')
def groundSegmentLog():
    return render_template('ground-segment-log.html')

@application.route('/ground-segment-status.html')
def groundSegmentStatus():
    return render_template('ground-segment-status.html')

@application.route('/commands-fan-on.html')
def commandsFanOn():
    global counter_request_number
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Ground_Commands_To_Spacecraft')
   
    autonomy_status=0
    fan_speed=1000

    response = table.put_item(
        Item={
            'Request_Number': str(counter_request_number),
            'Autonomy_status': autonomy_status,
            'Fan_Speed': fan_speed
        }
    )
    counter_request_number=counter_request_number + 1
    
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    return render_template('commands-fan-on.html')

@application.route('/commands-fan-off.html')
def commandsFanOff():
    global counter_request_number
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Ground_Commands_To_Spacecraft')
   
    autonomy_status=0
    fan_speed=1000

    response = table.put_item(
        Item={
            'Request_Number': str(counter_request_number),
            'Autonomy_status': autonomy_status,
            'Fan_Speed': fan_speed
        }
    )
    counter_request_number=counter_request_number + 1
    
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    return render_template('commands-fan-off.html')

@application.route('/autonomy-mode-commands.html')
def autoCommands():
    global counter_request_number
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Ground_Commands_To_Spacecraft')
   
    autonomy_status=1
    fan_speed=1000

    response = table.put_item(
        Item={
            'Request_Number': str(counter_request_number),
            'Autonomy_status': autonomy_status,
            'Fan_Speed': fan_speed
        }
    )
    counter_request_number=counter_request_number + 1
    
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    return render_template('autonomy-mode-commands.html')

@application.route('/about-insects.html')
def aboutInsects():
    return render_template('about-insects.html')

@application.route('/about-the-team.html')
def abouttheteam():
    return render_template('about-the-team.html')

#@application.errorhandler(401)
#def error401():
#    return render_template('401.html')

#@application.errorhandler(404)
#def error404():
#    return render_template('404.html')

#@application.errorhandler(500)
#def error500():
#    return render_template('500.html')

if __name__=="__main__":
    application.run(debug=True)

