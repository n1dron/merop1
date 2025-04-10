import React from 'react';
import styles from './EventList.module.css';

const EventList = ({ events }) => {
  return (
    <div className={styles.list}>
      {events.map(event => (
        <div key={event.id} className={styles.card}>
          <h3>
            <a href={`/events/${event.id}`}>{event.title}</a>
          </h3>
          <p>Вид спорта: {event.sport_type}</p>
          <p>Дата: {event.date}</p>
          <p>Место: {event.location}</p>
        </div>
      ))}
    </div>
  );
};

export default EventList;