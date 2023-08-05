from slacktastic.client import SlackClient
from slacktastic.template import Message, PieChart, BarChart

client = SlackClient(
    webhook_url='https://hooks.slack.com/services/'
                'TBWAF1BH7/BLTGSMRNK/40X6YJP7czgUX4OgSfGvFlUR')

test = PieChart(
    "Test data", labels=['Ride', 'Reservation'], values=[22, 55])

test_2 = BarChart(
    "Test data", labels=['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    data={
        'Test 1': [1, 2, 4, 8, 16],
        'Test 2': [7, 3, 45, 1, 12],
    })

message = Message(text='This is a *test*', attachments=[test, test_2])
client.send_message(message)
