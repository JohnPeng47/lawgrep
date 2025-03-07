import React, { useEffect, useState, useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Fuse from 'fuse.js';
import apiClient, { CourtRuling, QueryResults } from '../api/apiClient';
import SideMenu from '../components/SideMenu';
import CourtRulingList from '../components/CourtRulingList';

function SearchResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [queryResults, setQueryResults] = useState<QueryResults | null>(null);
  const [localSearchTerm, setLocalSearchTerm] = useState('');
  const [fuse, setFuse] = useState<Fuse<CourtRuling> | null>(null);
  const [filteredDocs, setFilteredDocs] = useState<CourtRuling[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Parse ?query= from the URL
  const searchParams = new URLSearchParams(location.search);
  const mainQuery = searchParams.get('query');

  // On mount: fetch rulings for mainQuery
  useEffect(() => {
    setIsLoading(true);
    if (!mainQuery) {
      navigate('/'); // If no query, redirect to home
      return;
    }
    
    apiClient.fetchLegalRulings(mainQuery).then(data => {
      setQueryResults(data);
      setFilteredDocs(data.rulings);
      
      // Initialize fuse with the returned documents
      const options = {
        keys: Object.keys(data.rulings[0]?.displayViews || {}).map(key => `displayViews.${key}`),
        includeScore: true,
        threshold: 0.4, // adjust to taste
      };
      
      const fuseInstance = new Fuse(data.rulings, options);
      setFuse(fuseInstance);
      setIsLoading(false);
    });
  }, [mainQuery, navigate]);

  // Use a local search to filter documents with Fuse
  useEffect(() => {
    if (!fuse || !queryResults) return;
    
    if (localSearchTerm.trim() === '') {
      // If no local search, show all
      setFilteredDocs(queryResults.rulings);
    } else {
      const results = fuse.search(localSearchTerm);
      // each result has .item with the original doc
      setFilteredDocs(results.map(r => r.item));
    }
  }, [localSearchTerm, fuse, queryResults]);

  // The side menu might also filter by issues or change the displayView
  const [selectedIssues, setSelectedIssues] = useState<string[]>([]);
  const [selectedDisplayView, setSelectedDisplayView] = useState<string | null>(null);

  // Final filtered docs, factoring in side menu filters as well
  const finalDocs = useMemo(() => {
    // e.g. if selectedIssues is non-empty, filter out docs that don't match
    if (!filteredDocs) return [];
    if (selectedIssues.length === 0) return filteredDocs;
    return filteredDocs.filter(doc =>
      doc.issues.some(issue => selectedIssues.includes(issue))
    );
  }, [filteredDocs, selectedIssues]);

  const handleToggleIssue = (issue: string) => {
    setSelectedIssues(prev => 
      prev.includes(issue) ? prev.filter(i => i !== issue) : [...prev, issue]
    );
  };

  if (isLoading) {
    return <div className="loading-container">Loading...</div>;
  }

  if (!queryResults) {
    return <div className="error-container">No results found</div>;
  }

  return (
    <div className="search-result-page">
      <div className="top-search-bar">
        <input
          type="text"
          placeholder="Filter results..."
          value={localSearchTerm}
          onChange={(e) => setLocalSearchTerm(e.target.value)}
          className="filter-input"
        />
        <button className="home-button" onClick={() => navigate('/')}>Home</button>
      </div>
      
      <div className="results-container">
        <SideMenu
          legalIssues={queryResults.legalIssues}
          onToggleIssue={handleToggleIssue}
          displayViews={queryResults.availableDisplayViews || []}
          selectedDisplayView={selectedDisplayView}
          onSelectDisplayView={setSelectedDisplayView}
        />
        
        <CourtRulingList
          rulings={finalDocs}
          selectedDisplayView={selectedDisplayView}
          keywordFilter={localSearchTerm}
        />
      </div>
    </div>
  );
}

export default SearchResultPage;