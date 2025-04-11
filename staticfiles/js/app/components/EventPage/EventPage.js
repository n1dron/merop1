import React from 'react';
import { useParams } from 'react-router-dom';
import './EventPage.css';

const EventPage = ({ events }) => {
  const { id } = useParams();
  const event = events.find(e => e.id === parseInt(id));

  return (
    <div className="event-page">
      {/* Просто выводим данные как есть */}
      <h1>{event.title}</h1>
      <p><strong>Вид спорта:</strong> {event.sportType}</p>
      <p><strong>Дата и время:</strong> {event.date}</p>
      <p><strong>Место:</strong> {event.location}</p>
      <p>{event.description}</p>
    </div>
  );
};

export default EventPage;