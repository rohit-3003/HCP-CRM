import React, { useState } from 'react';
import { Save } from 'lucide-react';
import api from '../services/api';

const StructuredForm = () => {
  const [formData, setFormData] = useState({
    hcp_id: '',
    duration: 15,
    location: '',
    discussion_summary: '',
    sentiment: 'Neutral'
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      await api.post('/interactions', {
        ...formData,
        hcp_id: parseInt(formData.hcp_id) || 1
      });
      setMessage('Interaction logged successfully!');
      setFormData({ hcp_id: '', duration: 15, location: '', discussion_summary: '', sentiment: 'Neutral' });
    } catch (error) {
      setMessage('Failed to log interaction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Manual Entry</h2>
      </div>
      
      <div className="form-container">
        {message && (
          <div className={`insight-box ${message.includes('success') ? 'positive' : 'negative'}`} style={{marginBottom: '1rem'}}>
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>HCP ID</label>
            <input
              type="number"
              className="form-input"
              value={formData.hcp_id}
              onChange={(e) => setFormData({...formData, hcp_id: e.target.value})}
              placeholder="e.g., 1 for Dr. Priya Sharma"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Duration (mins)</label>
              <input
                type="number"
                className="form-input"
                value={formData.duration}
                onChange={(e) => setFormData({...formData, duration: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                className="form-input"
                value={formData.location}
                onChange={(e) => setFormData({...formData, location: e.target.value})}
                placeholder="e.g., Clinic"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Sentiment</label>
            <select
              className="form-select"
              value={formData.sentiment}
              onChange={(e) => setFormData({...formData, sentiment: e.target.value})}
            >
              <option value="Positive">Positive</option>
              <option value="Neutral">Neutral</option>
              <option value="Negative">Negative</option>
            </select>
          </div>

          <div className="form-group">
            <label>Discussion Summary</label>
            <textarea
              className="form-textarea"
              rows="4"
              value={formData.discussion_summary}
              onChange={(e) => setFormData({...formData, discussion_summary: e.target.value})}
              placeholder="Details of the interaction..."
              required
            ></textarea>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="submit-btn"
          >
            <Save size={18} />
            {loading ? 'Saving...' : 'Save Interaction'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default StructuredForm;
