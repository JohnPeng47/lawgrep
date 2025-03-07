import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient, { SavedQuery } from '../api/apiClient';

function HomePage() {
  const navigate = useNavigate();
  const [previousQueries, setPreviousQueries] = useState<SavedQuery[]>([]);
  const [newQuery, setNewQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch previously searched queries from server
    setIsLoading(true);
    apiClient.getSavedQueries().then(data => {
      setPreviousQueries(data);
      setIsLoading(false);
    });
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newQuery.trim()) {
      // Navigate to results page with the new query
      navigate(`/results?query=${encodeURIComponent(newQuery.trim())}`);
    }
  };

  const handleLoadSavedQuery = (savedQuery: SavedQuery) => {
    // Navigate to results page with the saved query
    navigate(`/results?query=${encodeURIComponent(savedQuery.queryText)}`);
  };

  return (
    <div className="home-page">
      <h1>Retro-Future Legal Search</h1>
      <form onSubmit={handleSubmit} className="search-form">
        <input
          value={newQuery}
          onChange={(e) => setNewQuery(e.target.value)}
          placeholder="Enter your legal query..."
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
      </form>

      <div className="previous-queries-container">
        <h2>Previously Searched</h2>
        {isLoading ? (
          <div className="loading">Loading...</div>
        ) : (
          <div className="saved-queries-list">
            {previousQueries.map((q) => (
              <div key={q.id} className="saved-query-item" onClick={() => handleLoadSavedQuery(q)}>
                {q.name || q.queryText}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default HomePage;