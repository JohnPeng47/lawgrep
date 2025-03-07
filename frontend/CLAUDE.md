Below is an updated architecture outline incorporating your new requirements:

Two-page flow using a client-side router (for example, React Router).
Page 1: “Home” (initial search page) – displays:
A search bar for the user to enter a new query.
A list of previously searched queries (retrieved from the backend).
Page 2: “SearchResultPage” – displays:
A top bar with a local search input (client-side keyword filter).
A SideMenu for filtering by legal issues and switching display views.
A CourtRulingList in the main area, with cards for each ruling.
Finally, we’ll highlight how client-side keyword search can be done in parallel using a library like Fuse.js or lunr.

1. Routing Structure
You can use React Router v6 (or newer) with a minimal BrowserRouter setup:

jsx
Copy
Edit
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SearchResultPage from './pages/SearchResultPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/results" element={<SearchResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
HomePage Component
Purpose:

Fetches a list of previously saved queries from the backend (via GET /api/savedQueries, for example).
Displays them in a list or grid.
Has a main search bar for the user’s new query.
When the user submits the search, navigate to “/results?query=...”.
Pseudo-code snippet:

jsx
Copy
Edit
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient'; // hypothetical API client

function HomePage() {
  const navigate = useNavigate();
  const [previousQueries, setPreviousQueries] = useState([]);
  const [newQuery, setNewQuery] = useState('');

  useEffect(() => {
    // Fetch previously searched queries from server
    apiClient.getSavedQueries().then(data => {
      setPreviousQueries(data);
    });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newQuery.trim()) {
      // Navigate to results page with the new query
      navigate(`/results?query=${encodeURIComponent(newQuery.trim())}`);
    }
  };

  const handleLoadSavedQuery = (savedQuery) => {
    // Navigate to results page with the saved query
    navigate(`/results?query=${encodeURIComponent(savedQuery.queryText)}`);
  };

  return (
    <div className="home-page">
      <h1>Retro-Future Legal Search</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={newQuery}
          onChange={(e) => setNewQuery(e.target.value)}
          placeholder="Enter your legal query..."
        />
        <button type="submit">Search</button>
      </form>

      <div className="previous-queries-container">
        <h2>Previously Searched</h2>
        {previousQueries.map((q) => (
          <div key={q.id} className="saved-query-item" onClick={() => handleLoadSavedQuery(q)}>
            {q.name || q.queryText}
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
CSS Snippet (for a “retro/futuristic/gamey” look, using Roboto Mono):

css
Copy
Edit
.home-page {
  font-family: 'Roboto Mono', monospace;
  color: #00ff99; /* Neon green text */
  background: #1c1c1c; /* Dark background for futuristic vibe */
  padding: 2rem;
}

.home-page h1 {
  font-size: 2rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.home-page input {
  background: #222;
  border: none;
  border-bottom: 2px solid #00ff99;
  color: #fff;
  padding: 0.5rem;
  margin-right: 1rem;
}

.saved-query-item {
  cursor: pointer;
  margin: 0.5rem 0;
  transition: color 0.2s;
}
.saved-query-item:hover {
  color: #00ffff; /* subtle highlight on hover */
}
SearchResultPage Component
Purpose:

Retrieve the main query from the URL (/results?query=...).
Make an API call to get the relevant rulings (like apiClient.fetchLegalRulings(query)).
Render:
a local filter search bar (for client-side keyword searching),
a SideMenu with issues and display-view switching,
a CourtRulingList that actually shows the filtered results.
Pseudo-code:

jsx
Copy
Edit
import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState, useMemo } from 'react';
import apiClient from '../api/apiClient';
import SideMenu from '../components/SideMenu';
import CourtRulingList from '../components/CourtRulingList';
import * as Fuse from 'fuse.js'; // or 'lunr'

function SearchResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [queryResults, setQueryResults] = useState(null);
  const [localSearchTerm, setLocalSearchTerm] = useState('');
  const [fuse, setFuse] = useState(null); // fuse instance for parallel searching
  const [filteredDocs, setFilteredDocs] = useState([]);

  // Parse ?query= from the URL
  const searchParams = new URLSearchParams(location.search);
  const mainQuery = searchParams.get('query');

  // On mount: fetch rulings for mainQuery
  useEffect(() => {
    if (!mainQuery) {
      navigate('/'); // If no query, redirect to home
      return;
    }
    apiClient.fetchLegalRulings(mainQuery).then(data => {
      setQueryResults(data);
      // Initialize fuse with the returned documents
      const options = {
        keys: ['rulingSummary', 'keyFactors', 'someOtherView'], 
        includeScore: true,
        threshold: 0.4, // adjust to taste
      };
      const fuseInstance = new Fuse(data.rulings, options);
      setFuse(fuseInstance);
      setFilteredDocs(data.rulings);
    });
  }, [mainQuery, navigate]);

  // Use a local search to filter documents with Fuse
  useEffect(() => {
    if (!fuse) return;
    if (localSearchTerm.trim() === '') {
      // If no local search, show all
      setFilteredDocs(queryResults?.rulings || []);
    } else {
      const results = fuse.search(localSearchTerm);
      // each result has .item with the original doc
      setFilteredDocs(results.map(r => r.item));
    }
  }, [localSearchTerm, fuse, queryResults]);

  // The side menu might also filter by issues or change the displayView
  const [selectedIssues, setSelectedIssues] = useState([]);
  const [selectedDisplayView, setSelectedDisplayView] = useState(null);

  // Final filtered docs, factoring in side menu filters as well
  const finalDocs = useMemo(() => {
    // e.g. if selectedIssues is non-empty, filter out docs that don't match
    if (!filteredDocs) return [];
    if (selectedIssues.length === 0) return filteredDocs;
    return filteredDocs.filter(doc =>
      doc.issues.some(issue => selectedIssues.includes(issue))
    );
  }, [filteredDocs, selectedIssues]);

  if (!queryResults) {
    return <div>Loading...</div>;
  }

  return (
    <div className="search-result-page">
      <div className="top-search-bar">
        <input
          type="text"
          placeholder="Filter results..."
          value={localSearchTerm}
          onChange={(e) => setLocalSearchTerm(e.target.value)}
        />
      </div>
      <SideMenu
        legalIssues={queryResults.legalIssues}
        onToggleIssue={(issue) => {
          setSelectedIssues(prev => 
            prev.includes(issue) ? prev.filter(i => i !== issue) : [...prev, issue]
          );
        }}
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
  );
}

export default SearchResultPage;
CSS Snippet:

css
Copy
Edit
.search-result-page {
  display: flex;
  flex-direction: row;
  height: 100vh;
  font-family: 'Roboto Mono', monospace;
  color: #00ff99;
  background: #121212; 
}

.top-search-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 1rem;
  background: #222;
  z-index: 100;
  border-bottom: 2px solid #00ff99;
}

.top-search-bar input {
  width: 30%;
  padding: 0.5rem;
  background: #000;
  border: 1px solid #00ff99;
  color: #00ff99;
}
2. SideMenu
jsx
Copy
Edit
function SideMenu({
  legalIssues = [],
  onToggleIssue,
  displayViews = [],
  selectedDisplayView,
  onSelectDisplayView
}) {
  return (
    <div className="side-menu">
      <h2>Legal Issues</h2>
      {legalIssues.map(issue => (
        <div key={issue} className="issue-row">
          <input
            type="checkbox"
            onChange={() => onToggleIssue(issue)}
          />
          <label>{issue}</label>
        </div>
      ))}
      <h2>Display Views</h2>
      {displayViews.map(view => (
        <button
          key={view}
          disabled={view === selectedDisplayView}
          onClick={() => onSelectDisplayView(view)}
        >
          {view}
        </button>
      ))}
    </div>
  );
}
CSS Snippet:

css
Copy
Edit
.side-menu {
  width: 15rem;
  background: #1f1f1f;
  padding: 1rem;
  margin-top: 4rem; /* to avoid overlap with top-search-bar */
}

.side-menu h2 {
  color: #00ffff;
  margin-bottom: 1rem;
}

.issue-row {
  margin-bottom: 0.5rem;
}
3. CourtRulingList / CourtRulingCard
CourtRulingList
jsx
Copy
Edit
function CourtRulingList({
  rulings,
  selectedDisplayView,
  keywordFilter
}) {
  return (
    <div className="court-ruling-list">
      <h3>{rulings.length} documents matched</h3>
      {rulings.map(ruling => (
        <CourtRulingCard
          key={ruling.id}
          ruling={ruling}
          activeDisplayView={selectedDisplayView || ruling.defaultDisplayView}
          keywordFilter={keywordFilter}
        />
      ))}
    </div>
  );
}

export default CourtRulingList;
CourtRulingCard
jsx
Copy
Edit
import HighlightedText from './HighlightedText';

function CourtRulingCard({ ruling, activeDisplayView, keywordFilter }) {
  const textContent = ruling.displayViews[activeDisplayView] || '';

  return (
    <div className="court-ruling-card">
      <HighlightedText text={textContent} highlight={keywordFilter} />
      <div className="fade-out-overlay" />
    </div>
  );
}

export default CourtRulingCard;
CSS Snippet:

css
Copy
Edit
.court-ruling-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  margin-top: 4rem; /* again, account for top bar */
}

.court-ruling-card {
  position: relative;
  max-height: 200px;
  overflow: hidden;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #242424;
  border: 1px solid #00ff99;
  border-radius: 4px;
}

.fade-out-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50px;
  /* Create a vertical fade from transparent to the background color */
  background: linear-gradient(
    to bottom,
    rgba(36,36,36,0) 0%,
    rgba(36,36,36,1) 100%
  );
}
4. HighlightedText Component
jsx
Copy
Edit
function HighlightedText({ text, highlight }) {
  if (!highlight) return <>{text}</>;

  const regex = new RegExp(`(${highlight})`, 'gi');
  const parts = text.split(regex);

  return (
    <>
      {parts.map((part, index) => 
        regex.test(part) ? (
          <mark key={index}>{part}</mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </>
  );
}

export default HighlightedText;
CSS Snippet:

css
Copy
Edit
mark {
  background-color: #00ffff;
  color: #000000;
}
(This yields a neon-cyan highlight on a dark background, giving a “gamey” feel.)

5. Client-Side Keyword Search with Fuse.js (or Lunr)
The snippet in SearchResultPage shows how to create a Fuse instance for your entire list of rulings and re-run the search each time the user types a new keyword.
Because you store the entire dataset in memory on the client, the searching can happen rapidly in parallel. For large corpora, you may need to consider performance optimizations, but for moderate data sets, Fuse or Lunr is straightforward.
Sample Code with Lunr
If using Lunr, you’d build an index of your documents first. For example:

js
Copy
Edit
import lunr from 'lunr';

useEffect(() => {
  if (!queryResults) return;

  const builder = new lunr.Builder();
  builder.ref('id');
  builder.field('rulingSummary');
  builder.field('keyFactors');

  queryResults.rulings.forEach(r => {
    builder.add(r);
  });

  const idx = builder.build();
  setIndex(idx);
}, [queryResults]);
Then on each local search term change:

js
Copy
Edit
const results = idx.search(localSearchTerm); 
// returns array of refs, then map back to docs
Either library approach is quite similar.

Conclusion
This design meets all of your requirements:

HomePage (initial search + saved searches list).
SearchResultPage (side menu, card display, local search, etc.).
Client-side partial matching search with highlights using something like Fuse.js or Lunr.
Retro/futuristic design hints via CSS (neon colors, Roboto Mono font, dark backgrounds, etc.).
By splitting components clearly and handling routing from a dedicated App component, the user flow is straightforward:

User lands on Home → sees prior queries + main search bar → enters a query → navigates to “/results”.
Results Page → sees side menu, results list, local search filter on top → everything is done client-side for partial matching and dynamic filtering.





