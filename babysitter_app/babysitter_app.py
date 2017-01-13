from bottle import Bottle, redirect, request, route, static_file, template
import json
import dateutil.parser
import datetime

from constants.constants import CALENDAR_EVENTS_TEMPLATE, \
  CREATE_USER_FORM_TEMPLATE, \
  CREATE_USER_FAILURE_TEMPLATE, \
  GET_AVAILABILITIES_TEMPLATE, \
  HOME_TEMPLATE, \
  LOGIN_FAILURE_STRING, \
  LOGIN_FORM_TEMPLATE, \
  LOGIN_SUBMIT_TEMPLATE, \
  LOGOUT_FORM_TEMPLATE
from session import rw_session
from factory.user_bo_factory import UserBOFactory
from model.event import Event
from model.role import Role
from model.user import User
from model.user_role import UserRole

app = Bottle()

##################################
# routes
##################################
@app.route('/static/:path#.+#', name='static')
def static(path):
  """static file route
  """
  return static_file(path, root='static')

@app.route('/create-user')
def create_user_form():
  return template(CREATE_USER_FORM_TEMPLATE)

@app.route('/create-user', method='POST')
def create_user_submit():
  user_info = {}
  user_info['name'] = request.forms.get('name')
  user_info['email'] = request.forms.get('email')
  user_info['password'] = request.forms.get('password')

  user_address_info = {}
  user_address_info['street_no'] = request.forms.get('street_no')
  user_address_info['street_name'] = request.forms.get('street_name')
  user_address_info['city'] = request.forms.get('city')
  user_address_info['province'] = request.forms.get('province')
  user_address_info['postal_code'] = request.forms.get('postal_code')
  user_address_info['country'] = request.forms.get('country')

  user_type = None
  if request.forms.get('babysitter', None):
    user_type = Role.BABYSITTER_ROLE

  try:
    user = UserBOFactory.create_user_bo(
        user_type, user_info, user_address_info)
  except:
    return template(CREATE_USER_FAILURE_TEMPLATE)

  if not user:
    return template(CREATE_USER_FAILURE_TEMPLATE)
  return redirect("/login")

@app.route('/login')
def login_form():
  return template(LOGIN_FORM_TEMPLATE)

@app.route('/login', method='POST')
def login_submit():
  email = request.forms.get('email')
  password = request.forms.get('password')

  with rw_session() as session:
    user = User.get_user_by_email(session, email)
    if user and user.verify_password(password):
      is_babysitter = UserRole.is_babysitter(session, user.id)
      return template(HOME_TEMPLATE, {
        'is_babysitter': is_babysitter,
        'name': user.name,
        'user_id': user.id
      })

  return template(LOGIN_FORM_TEMPLATE, {
    'errors': LOGIN_FAILURE_STRING
  })

@app.route('/logout')
def logout_form():
  return template(LOGOUT_FORM_TEMPLATE)


def put_ymd_availabilities(ymd_availabilities, year, month, day, user):
  try:
    availabilities = ymd_availabilities[year][month][day]
    availabilities.add((user.id, user.name))
    ymd_availabilities[year][month][day] = availabilities
  except:
    # either the year is not set or the month is not set correctly
    # get or set the year
    year_months = ymd_availabilities.get(year, {})
    ymd_availabilities[year] = year_months
    year_month_days = ymd_availabilities[year].get(month, {})
    ymd_availabilities[year][month] = year_month_days

    availabilities = ymd_availabilities[year][month].get(day, set([]))
    availabilities.add((user.id, user.name))
    ymd_availabilities[year][month][day] = availabilities

  return ymd_availabilities


@app.route('/availabilities/host')
def get_availabilities_for_all_host():
  with rw_session() as session:
    events = Event.get_all_available_events_after_now(session)
    ymd_availabilities = {}

    for event in events:
      year = event.start_date.year
      month = event.start_date.month
      day = event.start_date.day

      ymd_availabilities = put_ymd_availabilities(
          ymd_availabilities, year, month, day, event.host)

  return template(GET_AVAILABILITIES_TEMPLATE, {
    'ymd_availabilities': ymd_availabilities
  })


@app.route('/availabilities/host/<host_id:int>')
def get_availabilities(host_id):
  events = Event.get_all_events(host_id)
  logged_in_user_id = request.cookies.get('user_id', None)

  if not logged_in_user_id:
    return redirect("/login")

  host_user = User.get_user_by_id(host_id)
  is_editable_str_boolean = str(host_id == int(logged_in_user_id)).lower()
  return template(CALENDAR_EVENTS_TEMPLATE, {
    'host_id': host_id,
    'host_name': host_user.name,
    'events': events,
    'currentDate': datetime.datetime.now().isoformat(),
    'is_editable': is_editable_str_boolean
  })


@app.route('/availabilities/host/create/<host_id:int>', method='POST')
def availabilities_submit(host_id):
  # validate if someone already booked within the time slot
  logged_in_user_id = request.cookies.get('user_id', None)
  if not logged_in_user_id:
    return redirect("/login")

  customer_id = None
  logged_in_user_id = int(logged_in_user_id)
  if logged_in_user_id != host_id:
    customer_id = logged_in_user_id

  json_info = json.load(request.body)
  event_id = json_info.get('eventId', None)
  start_date = json_info.get('startDate', None)
  end_date = json_info.get('endDate', None)

  response = {}
  # host is create a new event
  if not event_id and start_date and end_date:
    start_date = dateutil.parser.parse(start_date)
    end_date = dateutil.parser.parse(end_date)
    if not customer_id:
      response = Event.create_host_event(host_id, start_date, end_date)

  return json.dumps(response)

@app.route('/availabilities/host/update/<host_id:int>', method='POST')
def availabilities_update(host_id):
  # validate if someone already booked within the time slot
  logged_in_user_id = request.cookies.get('user_id', None)
  if not logged_in_user_id:
    return redirect("/login")

  customer_id = None
  logged_in_user_id = int(logged_in_user_id)
  if logged_in_user_id != host_id:
    customer_id = logged_in_user_id

  json_info = json.load(request.body)
  event_id = json_info.get('eventId', None)
  start_date = json_info.get('startDate', None)
  end_date = json_info.get('endDate', None)

  response = {}
  if event_id:
    # update the event
    event_id = int(event_id)
    if customer_id:
      response = Event.update_customer_event(
        event_id, host_id, start_date, end_date, customer_id)
    else:
      response = Event.update_host_event(
        event_id, host_id, start_date, end_date)

  return json.dumps(response)
