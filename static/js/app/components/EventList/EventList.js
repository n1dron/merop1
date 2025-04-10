import React from 'react';
import { Link } from 'react-router-dom';
import './EventList.css';

const EventList = ({ events }) => {
  // Временная функция для проверки клика
  const handleClick = (id) => {
    console.log('Clicked on event:', id); // Должно появляться в консоли при клике
  };

  return (
    <div className="event-list">
      {events.map(event => (
        <Link 
          to={`/event/${event.id}`} 
          key={event.id}
          className="event-card-link"
          onClick={() => handleClick(event.id)}
        >
          <div className="event-card">
            <h3>{event.title}</h3>
            <p>{event.date} | {event.location}</p>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default EventList;