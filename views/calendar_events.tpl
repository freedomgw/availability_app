<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<link href='/static/external_api/fullcalendar/fullcalendar.min.css' rel='stylesheet' />
<link href='/static/external_api/fullcalendar/fullcalendar.print.min.css' rel='stylesheet' media='print' />
<script src='/static/lib/moment.min.js'></script>
<script src='/static/lib/jquery.min.js'></script>
<script src="/static/lib/jquery.cookie.min.js"></script>
<script src='/static/external_api/fullcalendar/fullcalendar.min.js'></script>

<script>
  $(document).ready(function() {
    // build the calendar events
    var calendarEvents = []
    % for currEvent in events:
      var calendarEvent = {}
      % for key, value in currEvent.iteritems():
        calendarEvent["{{key}}"] = "{{value}}";
      % end
      calendarEvents.push(calendarEvent);
    % end

    var postHostUpdateFn = function(event, delta, revertFunc) {
      var postData = {
        eventId: event['id'],
        startDate: $.fullCalendar.moment(event['start']).toISOString(),
        endDate: $.fullCalendar.moment(event['end']).toISOString()
      };

      $.ajax({
        type: "POST",
        url: "/availabilities/host/update/" + {{host_id}},
        data: JSON.stringify(postData),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
          if (data.event_id === null) {
            revertFunc();
          }
        },
        failure: function(err) {
          revertFunc();
        }
      });
    };

    $('#calendar').fullCalendar({
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'agendaWeek,agendaDay'
      },
      defaultDate: "{{ currentDate }}",
      navLinks: true, // can click day/week names to navigate views
      selectable: true,
      selectHelper: true,
      select: function(start, end) {
        var eventData = {
          start: start,
          end: end
        };

        var postData = {
          startDate: $.fullCalendar.moment(start).toISOString(),
          endDate: $.fullCalendar.moment(end).toISOString()
        };

        // submit new event
        $.ajax({
          type: "POST",
          url: "/availabilities/host/create/" + {{host_id}},
          data: JSON.stringify(postData),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function(data) {
            eventData['id'] = data.event_id;
            eventData['title'] = data.title;
          },
          failure: function(err) {
            alert("An error has occured.");
          },
          async: false
        });

        if (eventData['id']) {
          $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
        }

        $('#calendar').fullCalendar('unselect');
      },

      eventClick: function(calEvent, jsEvent, view) {
        var postData = {
          eventId: calEvent.id,
          startDate: $.fullCalendar.moment(calEvent['start']).toISOString(),
          endDate: $.fullCalendar.moment(calEvent['end']).toISOString()
        };

        $.ajax({
          type: "POST",
          url: "/availabilities/host/update/" + {{host_id}},
          data: JSON.stringify(postData),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function(data) {
            var isCustomer = $.cookie("user_id") != {{ host_id }};
            if (data.event_id && isCustomer) {
              calEvent['title'] = data.title;
              calEvent['color'] = data.color;
              $('#calendar').fullCalendar('updateEvent', calEvent);
            } else if (isCustomer) {
              alert("Sorry! It looks like someone has already reserved this block! Please refresh the page!");
            } else {
              alert("You're the host! Don't reserve your own slots!");
            }
          },
          failure: function(err) {
            alert("An error has occured.");
          },
          async: false
        });
      },

      // events triggered by host
      eventDrop: postHostUpdateFn,
      eventResize: postHostUpdateFn,

      editable: {{ is_editable }},
      eventLimit: true, // allow "more" link when too many events
      events: calendarEvents,
      defaultView: "agendaWeek"
    });

  });
</script>

<style>
  body {
    margin: 40px 10px;
    padding: 0;
    font-family: "Lucida Grande",Helvetica,Arial,Verdana,sans-serif;
    font-size: 14px;
  }

  #calendar {
    max-width: 900px;
    margin: 0 auto;
  }
</style>
</head>

<body>

  <a href="/availabilities/host"><< View Other Available Hosts</a>
  <a href="/logout" style="float:right;">Logout</a>
  <h1 align="center">{{ host_name }}'s Baby Sitting Availabilities</h1>
  <div id='calendar'></div>

</body>
</html>
