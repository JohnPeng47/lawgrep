import React from 'react';

interface SideMenuProps {
  legalIssues: string[];
  onToggleIssue: (issue: string) => void;
  displayViews: string[];
  selectedDisplayView: string | null;
  onSelectDisplayView: (view: string) => void;
}

function SideMenu({
  legalIssues = [],
  onToggleIssue,
  displayViews = [],
  selectedDisplayView,
  onSelectDisplayView
}: SideMenuProps) {
  return (
    <div className="side-menu">
      <h2>Legal Issues</h2>
      {legalIssues.map(issue => (
        <div key={issue} className="issue-row">
          <input
            type="checkbox"
            onChange={() => onToggleIssue(issue)}
            id={`issue-${issue}`}
          />
          <label htmlFor={`issue-${issue}`}>{issue}</label>
        </div>
      ))}
      
      <h2>Display Views</h2>
      {displayViews.map(view => (
        <button
          key={view}
          className={`view-button ${view === selectedDisplayView ? 'selected' : ''}`}
          disabled={view === selectedDisplayView}
          onClick={() => onSelectDisplayView(view)}
        >
          {view}
        </button>
      ))}
    </div>
  );
}

export default SideMenu;