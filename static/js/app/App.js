import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import EventList from './components/EventList/EventList';
import EventPage from './components/EventPage/EventPage';

console.log('Router check:', { BrowserRouter, Routes, Route }); // Должны быть определены

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<EventList events={eventsData} />} />
          <Route path="/event/:id" element={<EventPage events={eventsData} />} />
        </Routes>
      </div>
    </Router>
  );
}

const App = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);

  // Загрузка данных при монтировании
  useEffect(() => {
    fetchEvents();
  }, []);
  
  const fetchEvents = async (params = {}) => {
    setLoading(true);
    try {
      const query = new URLSearchParams(params).toString();
      const response = await fetch(`/events/?${query}`);
      const data = await response.json();
      setEvents(data.events || []);
    } catch (error) {
      console.error('Ошибка загрузки:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = (formData) => {
    const params = {};
    // Убираем пустые значения
    if (formData.get('sport_type')) params.sport_type = formData.get('sport_type');
    if (formData.get('date_from')) params.date_from = formData.get('date_from');
    if (formData.get('date_to')) params.date_to = formData.get('date_to');
    
    fetchEvents(params);
  };

  if (loading) return <div>Загрузка...</div>;

  return (
    <div className="event-container">
      {events.length > 0 ? (
        events.map(event => (
          <div key={event.id} className="event-card">
            <h3>{event.title}</h3>
            <p><strong>Вид спорта:</strong> {event.sport_type?.name || event.sport_type || 'Не указан'}</p>
            <p><strong>Дата:</strong> {event.date} в {event.time}</p>
            <p><strong>Место:</strong> {event.location}</p>
            {event.description && <p>{event.description}</p>}
          </div>
        ))
      ) : (
        <div className="no-events">Мероприятий не найдено</div>
      )}
    </div>
    
  );
};