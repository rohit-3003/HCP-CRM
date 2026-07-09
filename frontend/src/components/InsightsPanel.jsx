import React from 'react';
import { useSelector } from 'react-redux';
import { Activity, AlertCircle, CheckCircle, FileText, Target, ShieldAlert } from 'lucide-react';

const InsightsPanel = () => {
  const { aiInsights } = useSelector((state) => state.chat);

  const getSentimentClass = (sentiment) => {
    if (!sentiment) return 'neutral';
    const s = sentiment.toLowerCase();
    if (s.includes('positive')) return 'positive';
    if (s.includes('negative')) return 'negative';
    return 'neutral';
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <Activity color="purple" size={20} />
        <span>AI Insights</span>
      </div>
      
      <div className="insights-content">
        {/* Summary Section */}
        <section className="insight-section">
          <h3><FileText size={14} /> Summary</h3>
          <div className="insight-box">
            {aiInsights.summary || "No summary available yet. Chat with the agent to generate insights."}
          </div>
        </section>

        {/* Sentiment Section */}
        <section className="insight-section">
          <h3><Target size={14} /> Sentiment</h3>
          <span className={`badge ${getSentimentClass(aiInsights.sentiment)}`}>
            {aiInsights.sentiment || 'Unknown'}
          </span>
        </section>
        
        {/* Extracted Entities */}
        <section className="insight-section">
          <h3><CheckCircle size={14} /> Extracted Entities</h3>
          <div className="insight-box">
            {Object.keys(aiInsights.entities || {}).length > 0 ? (
              <ul className="entity-list">
                {Object.entries(aiInsights.entities).map(([key, value]) => {
                  if (key === 'confidence_scores' || key === 'missing_fields' || !value) return null;
                  return (
                    <li key={key}>
                      <span className="entity-key">{key.replace('_', ' ')}:</span>
                      <span className="entity-value">{value.toString()}</span>
                    </li>
                  )
                })}
              </ul>
            ) : (
              <span style={{color: 'var(--text-muted)', fontSize: '0.75rem'}}>Awaiting data...</span>
            )}
          </div>
        </section>

        {/* Missing Fields */}
        {aiInsights.missingFields && aiInsights.missingFields.length > 0 && (
          <section className="insight-section">
            <h3 style={{color: 'var(--warning-text)'}}><AlertCircle size={14} /> Missing Information</h3>
            <div style={{display: 'flex', flexWrap: 'wrap', gap: '8px'}}>
              {aiInsights.missingFields.map((field, idx) => (
                <span key={idx} className="badge warning">
                  {field.replace('_', ' ')}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* Confidence Scores */}
        {Object.keys(aiInsights.confidenceScores || {}).length > 0 && (
          <section className="insight-section">
            <h3><ShieldAlert size={14} /> Confidence</h3>
            <div>
              {Object.entries(aiInsights.confidenceScores).map(([field, score]) => (
                <div key={field} className="confidence-row">
                  <span className="entity-key">{field.replace('_', ' ')}</span>
                  <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
                    <div className="confidence-bar-bg">
                      <div 
                        className="confidence-bar-fill" 
                        style={{ 
                          width: `${score * 100}%`,
                          backgroundColor: score > 0.8 ? '#22c55e' : score > 0.5 ? '#eab308' : '#ef4444'
                        }}
                      ></div>
                    </div>
                    <span style={{fontWeight: 600, width: '32px', textAlign: 'right'}}>{(score * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
};

export default InsightsPanel;
