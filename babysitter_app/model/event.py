from sqlalchemy import Column, Date, ForeignKey, Integer, String, or_
from sqlalchemy.orm import relationship

import datetime

from main import Base
from session import rw_session

class Event(Base):

  STR_AVAILABLE = 'AVAILABLE'
  STR_OCCUPIED = 'OCCUPIED'
  COLOR_OCCUPIED = 'red'
  COLOR_AVAILABLE = 'rgb(58, 135, 173)'

  __tablename__ = "event"

  id = Column(Integer, primary_key=True)
  created_at = Column(Date, default=datetime.datetime.now())
  updated_at = Column(Date,
    default=datetime.datetime.now(),
    onupdate=datetime.datetime.now())
  customer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
  host_id = Column(Integer, ForeignKey('user.id'), nullable=False)
  start_date = Column(Date, nullable=False)
  end_date = Column(Date, nullable=False)

  customer = relationship("User", foreign_keys=[customer_id])
  host = relationship("User", foreign_keys=[host_id])

  def __init__(self, host_id, start_date, end_date, customer_id=None):
    self.host_id = host_id
    self.customer_id = customer_id
    self.start_date = start_date
    self.end_date = end_date

  def get_title(self):
    """Gets the event title

    Arguments:
    self -- Event object

    Returns:
    string -- title
    """
    if not self.customer:
      return Event.STR_AVAILABLE
    return Event.STR_OCCUPIED + ': '+ self.customer.name

  @staticmethod
  def query_all_events_by_host_id(session, host_id):
    """Get all events by the host id

    Arguments:
    session -- r/w session
    host_id -- int, user.id

    Returns:
    List of Events
    """
    q = session.query(Event)
    q = q.filter(Event.host_id == host_id)
    return q.all()

  @staticmethod
  def get_all_available_events_after_now(session):
    """Get all available events after now

    Arguments:
    session -- r/w session

    Returns:
    List of Events
    """
    q = session.query(Event)
    q = q.filter(Event.start_date >= datetime.datetime.now())
    q = q.filter(Event.customer_id == None)
    q = q.order_by(Event.start_date)
    return q.all()

  @staticmethod
  def get_all_events(host_id):
    """Returns all events with the expected response for the template

    Arguments:
    host_id -- int, user.id

    Returns:
    events_response -- list of dictionary, list of events response
    """
    events_response = [{}]
    with rw_session() as session:
      events = Event.query_all_events_by_host_id(session, host_id)
      events_response = Event.get_events_response(events)
    return events_response

  @staticmethod
  def get_events_response(events):
    """Generate event response for all events

    Arguments:
    events -- list of Event object

    Returns:
    events_response -- list of dictionary, list of events response
    """
    result = []
    for event in events:
      current_event = {
        'id': event.id,
        'start': event.start_date.isoformat(),
        'end': event.end_date.isoformat(),
        'title': event.get_title()
      }
      if event.customer_id:
        current_event['color'] = Event.COLOR_OCCUPIED
      result.append(current_event)

    return result

  @staticmethod
  def find_within_conflicting_events(
      session, host_id, target_date, exclude_event_id=None):
    """Return an event if the target date is within any other event

    Arguments:
    session -- rw session
    host_id -- int, user.id
    target_date -- datetime, target date
    exclude_event_id -- int, exclude this Event.id

    Returns:
    None or Event
    """
    q = session.query(Event)
    q = q.filter(Event.host_id == host_id)
    q = q.filter(Event.start_date < target_date)
    q = q.filter(target_date < Event.end_date)
    if exclude_event_id:
      q = q.filter(Event.id != exclude_event_id)
    return q.first()

  @staticmethod
  def find_inner_conflicting_events(
      session, host_id, start_date, end_date, exclude_event_id=None):
    """Return an event if there is an event within the start date and end date

    Arguments:
    session -- rw session
    host_id -- int, user.id
    target_date -- datetime, target date
    exclude_event_id -- int, exclude this Event.id

    Returns:
    None or Event
    """
    q = session.query(Event)
    q = q.filter(Event.host_id == host_id)
    q = q.filter(start_date < Event.start_date)
    q = q.filter(Event.end_date < end_date)
    if exclude_event_id:
      q = q.filter(Event.id != exclude_event_id)
    return q.first()

  @staticmethod
  def get_conflicting_event(
      session, host_id, start_date, end_date, exclude_event_id=None):
    """Return any event found within any other event or
    if there an event found within the start date and end date

    Arguments:
    session -- rw session
    host_id -- int, user.id
    target_date -- datetime, target date
    exclude_event_id -- int, exclude this Event.id

    Returns:
    None or Event
    """
    return Event.find_within_conflicting_events(
        session, host_id, start_date, exclude_event_id=exclude_event_id) or \
      Event.find_within_conflicting_events(
        session, host_id, end_date, exclude_event_id=exclude_event_id) or \
      Event.find_inner_conflicting_events(
        session, host_id, start_date, end_date, exclude_event_id=exclude_event_id)

  @staticmethod
  def get_event(session, event_id, host_id):
    """Get an event with the event id and host id

    Arguments:
    session -- rw session
    event_id -- int, event.id
    host_id -- int, user.id

    Returns:
    None or Event
    """
    q = session.query(Event)
    q = q.filter(Event.id == event_id)
    q = q.filter(Event.host_id == host_id)
    return q.first()

  @staticmethod
  def create_host_event(host_id, start_date, end_date):
    """Create a new event

    Arguments:
    host_id -- int, user.id
    start_date -- datetime, proposed start date by host
    end_date -- datetime, proposed end date by host

    Returns:
    response -- dict
    """
    response = {}
    with rw_session() as session:
      conflicting_event = Event.get_conflicting_event(
          session, host_id, start_date, end_date)

      if not conflicting_event:
        event = Event(host_id, start_date, end_date)
        session.add(event)
        session.flush()

        response['event_id'] = event.id
        response['title'] = event.get_title()

    return response

  @staticmethod
  def update_host_event(event_id, host_id, start_date, end_date):
    """Update the start and end date for a given event

    Arguments:
    event_id -- int, event.id
    host_id -- int, user.id
    start_date -- datetime, new proposed start date by host
    end_date -- datetime, new proposed end date by host

    Returns:
    response -- dict
    """
    response = {
      'event_id': None
    }
    with rw_session() as session:
      event = Event.get_event(session, event_id, host_id)
      if event:
        conflicting_event = Event.get_conflicting_event(
            session, host_id, start_date, end_date, exclude_event_id=event.id)

        if conflicting_event:
          return response

        # host updating the dates
        if start_date:
          event.start_date = start_date
        if end_date:
          event.end_date = end_date

        session.add(event)
        session.flush()

        response['event_id'] = event.id
        response['title'] = event.get_title()

    return response

  @staticmethod
  def update_customer_event(
        event_id, host_id, start_date, end_date, customer_id):
    """Update an event, triggered by customer. Customer is able to reserve
    and unreserve themselves for a given event

    Arguments:
    event_id -- int, event.id
    host_id -- int, user.id
    start_date -- datetime, new proposed start date by host
    end_date -- datetime, new proposed end date by host
    customer_id -- int, user.id

    Returns:
    response -- dict
    """
    response = {
      'event_id': None
    }
    with rw_session() as session:
      event = Event.get_event(session, event_id, host_id)
      if event:
        # customer unreserved
        if event.customer_id and event.customer_id == customer_id:
          event.customer_id = None
          response['color'] = Event.COLOR_AVAILABLE;
        # new customer reserved
        elif not event.customer_id:
          event.customer_id = customer_id
          response['color'] = Event.COLOR_OCCUPIED;
        # someone is trying to take someone's reservation
        else:
          return response

        session.add(event)
        session.flush()

        response['event_id'] = event.id
        response['title'] = event.get_title()

    return response
