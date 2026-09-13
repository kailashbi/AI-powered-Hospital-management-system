import api from './api';

export const kafkaService = {
  getStatus: async () => {
    const response = await api.get('/kafka/status');
    return response.data;
  },

  getEvents: async (topic = null, limit = 50) => {
    const params = {};
    if (topic) params.topic = topic;
    if (limit) params.limit = limit;
    const response = await api.get('/kafka/events', { params });
    return response.data;
  },

  publishEvent: async (topic, eventType, payload) => {
    const response = await api.post('/kafka/publish', {
      topic,
      event_type: eventType,
      payload,
    });
    return response.data;
  },
};
