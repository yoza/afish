/**  react component **/
var EventDetails = React.createClass({
  displayName: 'EventDetails',

  render: function() {
    if (this.props.event) {
      var event = this.props.event;
      var instances = [];

      for (var i = 0; i < event.instances.length; i += 1) {
        var instance = event.instances[i];

        instances.push(
          <tr key={instance.id}>
            <td>{instance.start}</td>
            <td>{instance.place.name}</td>
            <td>{instance.place.city.name}</td>
          </tr>
        );
      }

      return <div className='event-details'>
        <h1>{event.title}</h1>
        <p>{event.description}</p>
        <table>
          <tbody>
            {instances}
          </tbody>
        </table>
      </div>;
    } else {
      return <div className='event-details'>No event selected</div>;
    }
  }
});

var EventsList = React.createClass({

  displayName: 'EventsList',

  getInitialState: function(props) {
    return {
      events: null,
      selectedEvent: null
    };
  },

  componentDidMount: function() {
    this.loadEvents();
  },

  onClick: function (event, e) {
    this.setState({
      selectedEvent: event
    })
  },

  loadEvents: function (url) {
    $.getJSON(url || '/api/events/', (function (data) {
        this.setState({events: data})
    }).bind(this));
  },

  render: function() {
    var items = [];

    if (this.state.events) {
      var events = this.state.events;

      for (var i = 0; i < events.results.length; i+=1) {
        var active = '';
        var event = events.results[i];
        if (event == this.state.selectedEvent) {
          // console.log(event)
          active = 'active';
        }
        items.push(
          <li  className={active} key={event.id} onClick={this.onClick.bind(this, event)}>
            <a>{event.title}</a>
          </li>
        );
      }

      return  <div className="events">
          <div className="events-wrap">
            <ul className='events-list'>
              {items}
            </ul>
            <EventDetails event={this.state.selectedEvent} />
          </div>
          <div className="pagination">
            {events.previous ?
              <a className="page" onClick={this.loadEvents.bind(this, events.previous)}>Previous</a>
              :
              <span>Previous</span>
            }
            {events.next ?
              <a className="page" onClick={this.loadEvents.bind(this, events.next)}>Next</a>
              :
              <span>Next</span>
            }

          </div>
      </div>;
    }

    return <div className="loading">Loading...</div>;
  }

});


React.render(
  <EventsList />,
  document.getElementById('poster-container')
);
